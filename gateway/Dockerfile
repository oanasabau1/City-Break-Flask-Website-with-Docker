FROM python:3.9

ENV EVENTS_SERVICE_URL=http://events:5000/events
ENV WEATHER_SERVICE_URL=http://weather:5000/weather

ENV DB_HOST=citybreak-db
ENV DB_USER=auth
ENV DB_PASSWORD=abc123

ADD . /gateway
WORKDIR /gateway

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]
