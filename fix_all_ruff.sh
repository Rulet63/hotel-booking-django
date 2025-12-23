#!/bin/bash

echo "=== Полная очистка кода Ruff ==="

echo "1. Добавление новых строк в конец файлов..."
find src/ -name "*.py" -exec sed -i -e '$a\' {} \;

echo "2. Удаление пробелов в пустых строках..."
find src/ -name "*.py" -exec sed -i 's/^[[:space:]]*$//' {} \;

echo "3. Автоматическое исправление..."
poetry run ruff check --fix src/

echo "4. Форматирование..."
poetry run ruff format src/

echo "5. Финальная проверка..."
poetry run ruff check src/

echo "=== Готово! ==="
