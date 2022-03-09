import os
import redis

from flask import Flask, jsonify


REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = int(os.getenv('REDIS_PORT'))
REDIS_PASS = os.getenv('REDIS_PASS')


app = Flask(__name__)


@app.route('/activeTargets')
def activeTargets():
    r = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT, 
            password=REDIS_PASS)

    active_targets = []
    for key in r.scan_iter("*"):
        last_active = r.get(key).decode()
        target = {
            'id': int(key.decode()),
            'last_active': last_active
        }
        active_targets.append(target)

    return jsonify(active_targets)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
