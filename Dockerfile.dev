# amorino/django-album
# Version: 1.0

# frontend
FROM node:8.11-alpine as front

WORKDIR /app

COPY ./frontend/package.json ./
COPY ./frontend/yarn.lock ./
RUN yarn install

COPY ./frontend ./

RUN yarn run build

# backend
FROM python:3.6
ENV PYTHONUNBUFFERED 1

ARG PROJECT=album
ARG PROJECT_DIR=/var/www/${PROJECT}

WORKDIR $PROJECT_DIR

COPY ./backend/Pipfile ./backend/Pipfile.lock ./
RUN pip install -U pipenv
RUN pipenv install --system

RUN mkdir ./static
COPY --from=front /app/dist ./static
COPY --from=front /app/webpack-stats-prod.json ./

COPY ./backend ./
COPY ./static ./static

COPY ./app-entrypoint.sh ./

ENTRYPOINT ["./app-entrypoint.sh"]
