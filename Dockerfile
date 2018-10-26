FROM python:3.6.2
ENV PYTHONUNBUFFERED 1

ARG PROJECT=album
ARG PROJECT_DIR=/var/www/${PROJECT}

WORKDIR $PROJECT_DIR

COPY ./backend/Pipfile ./backend/Pipfile.lock ./
RUN pip install -U pipenv
RUN pipenv install --system

COPY ./backend/ ./
