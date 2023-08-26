# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.10.12
FROM python:${PYTHON_VERSION}-slim as base

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

WORKDIR /app

ENV FLASK_APP=controller.py
ENV FLASK_RUN_PORT=8234
ENV FLASK_DEBUG=1
ENV FLASK_RUN_HOST=10x-weather-app

FROM base AS test
COPY test_integration.py requirements.tests.txt .
RUN python -m pip install -r requirements.tests.txt

FROM base AS app
COPY . .
RUN python -m pip install -r requirements.app.txt

EXPOSE 8234
CMD flask run
