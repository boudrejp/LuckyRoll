FROM python:3.7-alpine

# don't buffer outputs, and prints directly.. Helps with docker in Python
ENV PYTHONUNBUFFERED 1

# Install dependencies
COPY django.requirements.txt /requirements.txt
# --no-cache skips caching the index of the packages.
RUN apk update \
      && apk add --no-cache postgresql-client \
      && apk add --no-cache --virtual .tmp-build-deps \
      && apk add gcc libc-dev linux-headers postgresql-dev libffi-dev \
      && apk add --virtual build-deps musl-dev jpeg-dev zlib-dev 

RUN pip install -r /requirements.txt
RUN apk del .tmp-build-deps

WORKDIR /app
COPY ./app /app

RUN adduser -D user
USER user
