FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8
#https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker

MAINTAINER Fotone <jaemuon5582@gmail.com>

WORKDIR /app
RUN mkdir -p ./app

ADD ./app /app/app
COPY requirements.txt /tmp/requirements.txt

RUN apt-get clean
RUN apt-get update -y && apt-get install -y openjdk-11-jdk g++

RUN pip install --upgrade pip && pip install -r /tmp/requirements.txt

# install mecab
RUN curl -L https://raw.githubusercontent.com/konlpy/konlpy/master/scripts/mecab.sh | bash

# 디버그와 개발을 하기 위해서 아래와 같은 환경으로 실행시키기 권장
# docker run --name law-container -d -p 8000:80 -v $(pwd)/app:/app/app --link mysql-container:mysql  law-farm-app:latest /start-reload.sh
