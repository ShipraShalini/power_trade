# Reference: https://github.com/tiangolo/uvicorn-gunicorn-docker/blob/master/docker-images/python3.8.dockerfile
FROM python:3.11-slim-bullseye

WORKDIR /app

# Install build essentials in order to install gcc, & install poetry
RUN apt update && apt install build-essential -y && pip install --no-cache-dir -U poetry

COPY pyproject.toml .
COPY poetry.lock .

RUN poetry install

COPY power/ .

# Start Gunicorn with Uvicorn
CMD ["uvicorn", "main:app"]
