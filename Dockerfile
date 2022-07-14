# Base Image
FROM python:3.10.5-alpine

# Install Dependencies
RUN apk update \
	&& apk add gcc libffi-dev musl-dev postgresql-client

# Project Directory
WORKDIR /usr/src/app

# Environment Variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install Python Dependencies
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Uninstall Make Dependencies
RUN apk del gcc libffi-dev musl-dev

# Copy Project
COPY . .