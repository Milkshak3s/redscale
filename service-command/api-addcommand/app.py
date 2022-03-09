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


@app.route('/addCommand')
def addCommand():
    target = request.args.get('target',  type=int)
    command = request.args.get('command',  type=str)
    new_command = {
        'target': target,
        'command': command
    }

    # copy command to db
    engine = create_engine(f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}')
    if True:
        Base.metadata.create_all(engine)
    
    Session = sessionmaker(bind=engine)
    session = Session()

    command_sql = Command(target=target, pending=True, command=command)
    session.add(command_sql)
    session.commit()

    session.refresh(command_sql)
    new_command['id'] = command_sql.id

    # enqueue command
    rmq_queue = str(target)
    rmq = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    rmq_channel = rmq.channel()

    try:
        rmq_channel.queue_declare(queue=rmq_queue)
        rmq_channel.basic_publish(exchange='', routing_key=rmq_queue, body=json.dumps(new_command))
        rmq.close()
    except:
        return "Failed to queue", 400

    return jsonify(new_command)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
