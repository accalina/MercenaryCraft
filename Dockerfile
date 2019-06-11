FROM python:3.6
MAINTAINER Accalina

ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/merccraft
COPY . .

RUN pip install -r requirements.txt
RUN chmod 777 server.py