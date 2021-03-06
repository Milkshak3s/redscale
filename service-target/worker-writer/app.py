import json
import os
import pika
import redis
import sys
import time

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from lib import Base, Target


RABBITMQ_HOST = os.getenv('RABBITMQ_HOST')
RMQ_TARGET_QUEUE = os.getenv('RABBITMQ_HOST')

MYSQL_HOST =os.getenv('MYSQL_HOST')
MYSQL_PORT =os.getenv('MYSQL_PORT')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')

REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = int(os.getenv('REDIS_PORT'))
REDIS_PASS = os.getenv('REDIS_PASS')


def write_redis_value(key, value):
    r = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT, 
            password=REDIS_PASS)
    r.set(key, value)


def main():
    rmq = None
    try:
        rmq = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    except:
        time.sleep(5)
        rmq = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))

    rmq_channel = rmq.channel()
    rmq_channel.queue_declare(queue=RMQ_TARGET_QUEUE)

    def callback(ch, method, properties, body):
        target_data = json.loads(body)

        target_id = target_data.get('id')
        target_name = target_data.get('name', '')
        target_last_active = target_data.get('last_active')


        engine = create_engine(f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}')
        if True:
            Base.metadata.create_all(engine)
        
        Session = sessionmaker(bind=engine)
        session = Session()

        sql_target = session.query(Target).get(target_id)
        if sql_target is None:
            sql_target = Target(id=target_id, name=target_name, last_active=target_last_active)
        else:
            sql_target.last_active = target_last_active
            if target_name != '':
                sql_target.name = target_name

        session.commit()
        write_redis_value(target_id, target_last_active)
    
    rmq_channel.basic_consume(queue=RMQ_TARGET_QUEUE, on_message_callback=callback, auto_ack=True)
    rmq_channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
