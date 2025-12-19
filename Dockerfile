FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Копируем зависимости
COPY pyproject.toml poetry.lock ./

# Устанавливаем Poetry
RUN pip install poetry && \
    poetry config virtualenvs.create false

# Устанавливаем зависимости
RUN poetry install --no-interaction --no-ansi

# Копируем исходный код
COPY . .

# Создаем пользователя
RUN useradd -m -u 1000 django && \
    chown -R django:django /app
USER django

EXPOSE 8000

# Указываем Python где искать пакеты
ENV PYTHONPATH=/app/src

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "src.config.wsgi:application"]
