FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

COPY ./app/requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt

COPY ./start_celery.sh /
COPY ./start_celerybeat.sh /
COPY ./app /app
