FROM python:3.8

RUN apt update

WORKDIR /usr/src/app

ARG BUILD_ENV=production
ADD config/requirements ./requirements

RUN pip install --upgrade pip
RUN pip install --default-timeout=100 future
RUN pip install -r requirements/$BUILD_ENV.txt

ENV PYTHONPATH /usr/src/libs
ENV PYTHONPATH /usr/src/todoapp:$PYTHONPATH