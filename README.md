# 📋 Hotel Booking API

Django REST API для управления номерами отеля и бронированиями. Проект соответствует техническому заданию и включает все необходимые функции.

## 🚀 Быстрый старт

### Требования

* Docker и Docker Compose
* Python 3.12+ (для локальной разработки)

### Запуск проекта

```bash
# Клонировать репозиторий
git clone <repository-url>
cd hotel-booking-django

# Запустить проект через Docker Compose
docker compose up -d

# Применить миграции
docker compose exec web python manage.py migrate

# Создать суперпользователя (опционально)
docker compose exec web python manage.py createsuperuser
```

Проект будет доступен по адресу: [http://localhost:8000](http://localhost:8000)

---

## 📚 API Эндпоинты

### Управление номерами отеля

**Создание номера**

```bash
POST /rooms/
```

**Параметры:**

* `description` (string) - описание номера
* `price_per_night` (decimal) - цена за ночь

**Пример:**

```bash
curl -X POST http://localhost:8000/rooms/ \
  -H "Content-Type: application/json" \
  -d '{"description": "Люкс с видом на море", "price_per_night": 15000}'
```

**Ответ:**

```json
{
  "id": 1,
  "description": "Люкс с видом на море",
  "price_per_night": "15000.00",
  "created_at": "2024-01-01T10:00:00Z"
}
```

**Получение списка номеров**

```bash
GET /rooms/?ordering=price_per_night
```

**Параметры сортировки:**

* `ordering=price_per_night` или `-price_per_night`
* `ordering=created_at` или `-created_at`

**Ответ с пагинацией:**

```json
{
  "count": 10,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "description": "Стандартный номер",
      "price_per_night": "5000.00",
      "created_at": "2024-01-01T10:00:00Z"
    }
  ]
}
```

**Удаление номера**

```bash
DELETE /rooms/{id}/
```

Удаляются все связанные бронирования.

---

### Управление бронированиями

**Создание бронирования**

```bash
POST /bookings/create
```

**Параметры:**

* `room_id` (integer)
* `date_start` (YYYY-MM-DD)
* `date_end` (YYYY-MM-DD)

**Пример:**

```bash
curl -X POST -d "room_id=1&date_start=2024-12-25&date_end=2024-12-30" \
  http://localhost:8000/bookings/create
```

**Ответ:**

```json
{
  "booking_id": 1
}
```

**Удаление бронирования**

```bash
DELETE /bookings/{booking_id}/delete
```

**Получение бронирований номера**

```bash
GET /bookings/list?room_id={room_id}
```

**Ответ с пагинацией:**

```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "booking_id": 1,
      "date_start": "2024-12-25",
      "date_end": "2024-12-30"
    }
  ]
}
```

---

## 🛠 Разработка

**Локальная настройка**

```bash
poetry install
poetry shell
cp .env.example .env
python src/manage.py migrate
python src/manage.py runserver
```

**Запуск тестов**

```bash
docker compose exec web python -m pytest /app/tests/ -v
pytest tests/ -v  # локально
```

**Линтинг и форматирование**

```bash
ruff check src/
ruff format src/
python check_imports.py
```

---

## 📁 Структура проекта

```
src/
├── bookings/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   └── tests.py
├── rooms/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   └── tests.py
├── config/
│   ├── settings/
│   ├── urls.py
│   └── wsgi.py
└── manage.py
tests/
└── test_all.py
staticfiles/
Dockerfile
docker-compose.yml
pyproject.toml
Makefile
pytest.ini
README.md
```

---

## 🗄 База данных

PostgreSQL с индексами для фильтрации и сортировки:

```sql
-- bookings_booking_room_id_idx
-- bookings_booking_date_start_idx
-- rooms_hotelroom_created_at_idx
```

---

## 🔧 Технические особенности

* Пагинация через DRF
* Валидация дат и цен
* Проверка существования номера при бронировании
* Обработка ошибок в JSON

---

## 🧪 Тестирование

* Модели, сериализаторы и API полностью покрыты тестами.
* Статус тестов: все тесты проходят.

---

