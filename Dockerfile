# Base Image
FROM python:3.10.5-alpine

# Dependencies
RUN apk update \
	&& apk add postgresql-client

# Project Directory
WORKDIR /usr/src/app

# Environment Variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Python Dependencies
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Copy Project
COPY . .