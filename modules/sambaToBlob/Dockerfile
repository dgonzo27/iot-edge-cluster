# pull official base image
FROM python:3.9-slim-buster

# install system dependencies
RUN apt-get update && \
    apt-get install -y build-essential git

# set environment variables
ENV CURL_CA_BUNDLE /etc/ssl/certs/ca-certificates.crt
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# set working directory
WORKDIR /opt/src

# copy application files
COPY modules/sambaToBlob /opt/src/sambaToBlob
COPY common /opt/src/common

# install application dependencies
RUN pip install --upgrade pip
RUN pip install -e ./common -e ./sambaToBlob
