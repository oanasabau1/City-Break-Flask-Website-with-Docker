from flask import Flask, request
from flask_restful import Api, Resource

import json
import os
import datetime
import time
import redis

app = Flask('weather')
time.sleep(20)  #TODO
api = Api(app)
client = redis.Redis(host=os.environ.get('REDIS_HOST', 'redis'))


class Weather(Resource):
    def get(self):
        city = request.args.get("city")
        date = request.args.get("date", str(datetime.date.today()))
        key = f'{city}-{date}' if date else city
        weather = client.get(key)
        print(f'key={key}')
        if not weather:
            return [], 200

        try:
            weather = weather.decode('utf-8')
            weather = json.loads(weather)
        except json.JSONDecodeError:
            return 'Data format error', 500

        print(f'weather = {weather}')
        return json.dumps(weather), 200

    def post(self):
        keys = ('temperature', 'humidity', 'wind')
        weather = {k: request.form.get(k) for k in keys}
        city = request.form.get('city', 'Brasov')
        date = request.form.get('date', str(datetime.date.today()))
        key = f'{city}-{date}' if date else city
        try:
            client.set(key, json.dumps(weather))
        except Exception as e:
            print(f'Failed to set data in Redis: {e}')
            return 'Internal server error', 500

        return 'OK', 200


api.add_resource(Weather, '/weather')

weather = {
    'Brasov': {'temperature': 20, 'wind': 15, 'humidity': 50},
    'Timisoara': {'temperature': 40, 'wind': 0, 'humidity': 0}
}

if __name__ == '__main__':
    for city in weather.keys():
        client.set(city, json.dumps(weather[city]))

    app.run(host=os.environ.get('HOST', '0.0.0.0'), port=os.environ.get('PORT', 5000), debug=True)
