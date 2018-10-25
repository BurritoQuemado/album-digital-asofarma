FROM python:3.6
ENV PYTHONUNBUFFERED 1

ARG PROJECT=album
ARG PROJECT_DIR=/var/www/${album}

WORKDIR $PROJECT_DIR

COPY ./Pipfile ./Pipfile.lock ./
RUN pip install -U pipenv
RUN pipenv install --system

COPY ./ ./
