FROM python:3.8-alpine

# don't buffer outputs, and prints directly.. Helps with docker in Python
ENV PYTHONUNBUFFERED 1

# Install dependencies
COPY ./requirements.docker.txt /requirements.txt
# --no-cache skips caching the index of the packages.
RUN apk add --update --no-cache postgresql-client
RUN apk add --update --no-cache --virtual .tmp-build-deps \
      gcc libc-dev linux-headers postgresql-dev

RUN pip install -r /requirements.txt
RUN apk del .tmp-build-deps

WORKDIR /app
COPY ./api /app

RUN adduser -D user
USER user
