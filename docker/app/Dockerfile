FROM python:3.6

WORKDIR /src

ADD . /src
COPY . /src

RUN python setup.py develop

EXPOSE 8080