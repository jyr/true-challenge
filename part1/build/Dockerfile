FROM python:3.7-slim

ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install \
  -y --no-install-recommends python3-gdal wget python3-distutils && \
  pip install virtualenv

RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN virtualenv /code/env
ENV VIRTUAL_ENV=/code/env
RUN pip install -Ur requirements.txt
ADD . /code/
