FROM python:3.7-slim

ENV PYTHONUNBUFFERED 1

RUN \
    apt-get update && \
    apt-get -y install python3-gdal

RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/
