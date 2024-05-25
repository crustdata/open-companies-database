# Dockerfile
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE open_companies_database.settings_docker

# Set work directory
WORKDIR /code

# Install dependencies
COPY pyproject.toml /code/
COPY poetry.lock /code/
RUN pip install poetry
RUN poetry install --no-dev

# Copy project
COPY . /code/

