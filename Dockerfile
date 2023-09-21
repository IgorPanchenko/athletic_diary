FROM python:3.10-alpine3.18

COPY . /DjangoApp

WORKDIR /DjangoApp

EXPOSE 8000

RUN apk add postgresql-client build-base postgresql-dev

RUN pip install -r requirements.txt

RUN adduser --disabled-password user

USER user