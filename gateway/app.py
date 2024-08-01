from flask import *
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *

from flask_login import current_user, login_user, logout_user, UserMixin, LoginManager
from wtforms import *
from flask_session import Session


import json
import os
import logging
import datetime
import time

from requests import get as Get
from requests import post as Post
from requests import put as Put
from requests import delete as Delete

app = Flask('gateway')

DB_USER = os.environ.get('DB_USER') or 'event'
DB_PASS = os.environ.get('DB_PASSWORD') or 'abc123'
DB_HOST = os.environ.get('DB_HOST') or '127.0.0.1'  #prin 127.0.0.1 se conecteaza prin TCP, daca e localhost, se conecteaza prin sockets

db_url = f'mysql://{DB_USER}:{DB_PASS}@{DB_HOST}/auth'
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SESSION_TYPE'] = 'filesystem' #/var/www/flask_sessions/74623745326542452387452
app.config['SESSION_PERMANENT'] = True
app.secret_key='secretkey'

file_handler = logging.FileHandler('server.log')
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)

api = Api(app)
time.sleep(30)
db = SQLAlchemy(app)

events_url = os.environ.get('EVENTS_SERVICE_URL') #nu ii dam alternative, daca nu gaseste -> crapa
weather_url = os.environ.get('WEATHER_SERVICE_URL')

class CityBreak(Resource):
    def get(self):
        city = request.args.get('city')
        date = request.args.get('date', str(datetime.date.today()))
        if not city or not date:
            return 'Invalid request: city or date are missing', 400
        print(f'EVENTS_URL = {events_url}?city={city}&date={date}')
        print(f'WEATHER_ULR = {weather_url}?city={city}&date={date}')
        events = Get(f'{events_url}?city={city}&date={date}', verify=False).json()
        weather = Get(f'{weather_url}?city={city}&date={date}', verify=False).json()
        return {'events': events, 'weather': weather}, 200

api.add_resource(CityBreak, '/citybreak')

req_mapping = {'GET': Get, 'PUT': Put, 'POST': Post, 'DELETE' : Delete}

def proxy_request(request, target_url):
    req = req_mapping[request.method]
    kwargs = {'url': target_url, 'params': request.args}
    if request.method in ['PUT', 'POST']:
        kwargs['data'] = dict(request.form)
    response = req(**kwargs).json()
    return json.dumps(response)

@app.route('/events', methods=['POST', 'PUT', 'DELETE'])
def events():
    return proxy_request(request, events_url)

@app.route('/weather', methods=['POST', 'PUT', 'DELETE'])
def weather():
    return proxy_request(request, weather_url)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host=os.environ.get('HOST', '0.0.0.0'), port=os.environ.get('PORT', 5000) , debug=True)