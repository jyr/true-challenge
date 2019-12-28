FROM python:3.7-slim

ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install \
  -y --no-install-recommends python3-gdal wget python3-distutils iputils-ping git && \
  pip install virtualenv

RUN mkdir /code
WORKDIR /code

ADD aws /root/.aws
ADD . /code/

ENV VIRTUAL_ENV=/code/env
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
