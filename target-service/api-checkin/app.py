import json
import os
import pika
import time

from flask import Flask, jsonify, request


RABBITMQ_HOST = os.getenv('RABBITMQ_HOST')
RMQ_TARGET_QUEUE = os.getenv('RABBITMQ_HOST')


app = Flask(__name__)


@app.route('/checkIn', methods=['GET', 'POST'])
def activeTargets():
    target_id = request.args.get('id',  type=int)
    target_update = {
        'id': target_id,
        'last_active': time.time()
    }

    rmq = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    rmq_channel = rmq.channel()

    try:
        rmq_channel.queue_declare(queue=RMQ_TARGET_QUEUE)
        rmq_channel.basic_publish(exchange='', routing_key=RMQ_TARGET_QUEUE, body=json.dumps(target_update))
        rmq.close()
    except:
        return "Failed to send", 400

    return jsonify(target_update)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
