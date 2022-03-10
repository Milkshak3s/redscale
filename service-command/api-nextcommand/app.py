import json
import os
import pika

from flask import Flask, jsonify, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from lib import Base, Command


MYSQL_HOST =os.getenv('MYSQL_HOST')
MYSQL_PORT =os.getenv('MYSQL_PORT')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')

RABBITMQ_HOST = os.getenv('RABBITMQ_HOST')


app = Flask(__name__)


@app.route('/nextCommand')
def nextCommand():
    target = request.args.get('target',  type=int)

    # read command from queue
    rmq_queue = str(target)

    rmq = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    rmq_channel = rmq.channel()
    rmq_channel.queue_declare(queue=rmq_queue)

    # TODO: Really need to put the mysql writer in a different service, lots of reads on this need to be *fast*
    command = None
    method_frame, header_frame, body = rmq_channel.basic_get(queue=rmq_queue)
    if method_frame is None or method_frame.NAME == 'Basic.GetEmpty':
        rmq.close()
    else:
        rmq_channel.basic_ack(delivery_tag=method_frame.delivery_tag)
        rmq.close() 
        command = json.loads(body)
        command_id = command.get('id')

        # update pending value in db
        engine = create_engine(f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}')
        if True:
            Base.metadata.create_all(engine)
        
        Session = sessionmaker(bind=engine)
        session = Session()

        sql_target = session.query(Command).get(command_id)
        if sql_target is not None:
            sql_target.pending = False
            session.commit()

    return jsonify(command)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
