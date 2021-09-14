FROM python:3.8

WORKDIR /usr/src/app

ARG BUILD_ENV=production
ADD requirements ./requirements

RUN pip install --upgrade pip
RUN pip install -r requirements/$BUILD_ENV.txt