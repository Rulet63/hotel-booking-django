FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN pip install poetry && \
    poetry config virtualenvs.create false

RUN poetry install --no-interaction --no-ansi --no-root

COPY . .

# Меняем рабочую директорию на src, где manage.py
WORKDIR /app/src

RUN useradd -m -u 1000 django && \
    chown -R django:django /app

USER django

CMD ["sh", "-c", "python manage.py runserver 0.0.0.0:8000"]
