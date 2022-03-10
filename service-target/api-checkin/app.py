import json
import requests
import os
import pika
import time

from flask import Flask, jsonify, request


RABBITMQ_HOST = os.getenv('RABBITMQ_HOST')
RMQ_TARGET_QUEUE = os.getenv('RABBITMQ_HOST')

COMMAND_SERVICE_HOST = os.getenv('COMMAND_SERVICE_HOST')
COMMAND_SERVICE_PORT = os.getenv('COMMAND_SERVICE_PORT')
COMMAND_SERVICE_PROTOCOL = os.getenv('COMMAND_SERVICE_PROTOCOL')
NEXT_COMMAND_URI = "nextCommand"


app = Flask(__name__)


@app.route('/checkIn', methods=['GET', 'POST'])
def activeTargets():
    target_id = request.args.get('id',  type=int)
    if target_id is None or type(target_id) is not int:
        return "Requires argument id (int)", 400

    target_update = {
        'id': target_id,
        'last_active': time.time()
    }

    # send changes to write into queue
    rmq = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    rmq_channel = rmq.channel()

    try:
        rmq_channel.queue_declare(queue=RMQ_TARGET_QUEUE)
        rmq_channel.basic_publish(exchange='', routing_key=RMQ_TARGET_QUEUE, body=json.dumps(target_update))
        rmq.close()
    except:
        return "Failed to send", 400
    
    # pull next command (if available)
    r = requests.get(f'{COMMAND_SERVICE_PROTOCOL}://{COMMAND_SERVICE_HOST}:{COMMAND_SERVICE_PORT}/{NEXT_COMMAND_URI}?target={target_id}')
    json_response = r.json()
    if json_response is None:
        return jsonify(None)

    return jsonify(json_response)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
