FROM python:3.11.8-slim

RUN apt-get update && pip install --upgrade pip && pip install pipenv

WORKDIR /api

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=api.settings

COPY Pipfile* ./
RUN pipenv install --deploy --system --ignore-pipfile

COPY . .
