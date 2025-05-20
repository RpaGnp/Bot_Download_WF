FROM python:3.10-alpine

ENV PYTHONUNBUFFERED 1
ENV PATH="/scripts:${PATH}"

RUN cp /usr/share/zoneinfo/America/Bogota /etc/localtime

COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache libxslt openblas libstdc++ dos2unix

# Install Selenium dependencies
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc g++ linux-headers libc-dev libxml2-dev libxslt-dev libffi-dev python3-dev \
    libressl-dev libxml2 libxslt-dev libjpeg-turbo-dev zlib-dev \
    gfortran build-base freetype-dev libpng-dev openblas-dev \
    && pip install --upgrade pip \
    && pip install -r requirements.txt \
    && apk del .tmp-build-deps

# Install Selenium
RUN apk add --no-cache nodejs npm
RUN npm install -g chromedriver
RUN apk add --no-cache chromium

RUN apk update && apk add bash

RUN mkdir /app
WORKDIR /app
COPY ./app /app
COPY ./scripts /scripts

RUN chmod +x /scripts/* && dos2unix /scripts/*

RUN crontab /scripts/crontab.txt

ENTRYPOINT ["/scripts/entrypoint.sh"]
# ENTRYPOINT ["python", "/app/app.py"]