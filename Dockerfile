FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-root

COPY . .

WORKDIR /app/src

RUN useradd -m -u 1000 django

RUN mkdir -p /app/src/static && \
    mkdir -p /app/src/media && \
    chown -R django:django /app/src/static /app/src/media

USER django

CMD ["sh", "-c", "python manage.py migrate && uvicorn config.asgi:application --host 0.0.0.0 --port 8000 --workers 5"]