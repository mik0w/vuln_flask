# pull official base image
FROM python:3.9.1-slim-buster

# set work directory
WORKDIR /usr/src/app

# install system dependencies
RUN apt-get update && apt-get install bash

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

# copy project
COPY . /usr/src/app/

