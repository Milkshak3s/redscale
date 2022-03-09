import os

from flask import Flask, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from lib import Base, Command


MYSQL_HOST =os.getenv('MYSQL_HOST')
MYSQL_PORT =os.getenv('MYSQL_PORT')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')


app = Flask(__name__)


@app.route('/commandHistory')
def commandHistory():
    engine = create_engine(f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}')
    if True:
        Base.metadata.create_all(engine)
    
    Session = sessionmaker(bind=engine)
    session = Session()

    query = session.query(Command).all()
    commands = []
    for item in query:
        command = {
            'id': item.id,
            'target': item.target,
            'command': item.command,
            'pending': item.pending
        }
        commands.append(command)

    return jsonify(commands)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
