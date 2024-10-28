FROM python:3.12

LABEL maintainer="Kshitij <gk.kshitij@gmail.com>"

COPY ./backend/requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY ./backend/celery /celery_tasks
WORKDIR /celery_tasks

ENTRYPOINT celery -A tasks worker --loglevel=info