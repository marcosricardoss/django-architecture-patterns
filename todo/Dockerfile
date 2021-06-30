FROM python:3.8

RUN apt update

# app folders
WORKDIR /usr/src/app

# python installation

ARG BUILD_ENV=production
ADD config/requirements ./requirements

RUN pip install --upgrade pip
RUN pip install --default-timeout=100 future
RUN pip install -r requirements/$BUILD_ENV.txt

# scripts

ADD wait-for-it ./wait-for-it
ADD manage.py ./manage.py
ADD start ./start

# tests setup
ADD setup.cfg ./setup.cfg