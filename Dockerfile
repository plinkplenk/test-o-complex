FROM python:3.12.2-alpine AS base
WORKDIR /app
ENV PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

RUN apk add --update --no-cache --virtual .tmp-build-deps \
    build-base libc-dev linux-headers \
    && apk add libffi-dev \
    && apk add bash

RUN pip install poetry && poetry config virtualenvs.create false

COPY . .
COPY docker-entrypoint.sh /docker-entrypoint.sh

RUN poetry install --no-dev --no-interaction

WORKDIR ./weather

EXPOSE 8000

ENTRYPOINT ["/docker-entrypoint.sh"]
