FROM python

ENV REDIS_HOST=redis

ADD . /weather
WORKDIR /weather

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]