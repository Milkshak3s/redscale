import os

from flask import Flask, jsonify, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from lib import Base, Target


MYSQL_HOST =os.getenv('MYSQL_HOST')
MYSQL_PORT =os.getenv('MYSQL_PORT')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_ROOT_PASSWORD = os.getenv('MYSQL_ROOT_PASSWORD')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')


app = Flask(__name__)


@app.route('/target', methods=['GET'])
def target():
    target_id = request.args.get('id',  type=int)

    engine = create_engine(f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}')
    if True:
        Base.metadata.create_all(engine)
    
    Session = sessionmaker(bind=engine)
    session = Session()

    instance = session.query(Target).get(target_id)
    # if query.count() == 0:
    #     return "Query returned nothing", 400
    if instance is None:
        return f"Target {target_id} not found", 400

    fancy_target = {
        'id': instance.id,
        'name': instance.name,
        'last_active': instance.last_active
    }

    return jsonify(fancy_target)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
