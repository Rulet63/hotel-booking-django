import logging
from datetime import date, timedelta

import pytest
from django.utils import timezone
from rest_framework.test import APIClient

from bookings.models import Booking
from rooms.models import HotelRoom
from rooms.serializers import HotelRoomSerializer

logger = logging.getLogger(__name__)


def log_response(test_name, response, success_status=201, key=None):
    """Универсальное логирование для тестов."""
    if response.status_code == success_status:
        msg = f"{test_name}: успешно"
        if key and key in response.data:
            msg += f", {key}={response.data[key]}"
        logger.info(msg)
    else:
        logger.error(f"{test_name}: ошибка, статус={response.status_code}, ответ={response.data}")


@pytest.mark.django_db
def test_1_model_room():
    room = HotelRoom.objects.create(
        description="Тестовый номер отеля с описанием",
        price_per_night=5000.00
    )
    assert room.id is not None
    logger.info("Тест 1: Модель номера - успешно создана, id=%s", room.id)


@pytest.mark.django_db
def test_2_model_booking():
    room = HotelRoom.objects.create(
        description="Номер для теста бронирования",
        price_per_night=5000.00
    )
    booking = Booking.objects.create(
        room=room,
        date_start=date(2025, 6, 1),
        date_end=date(2025, 6, 3)
    )
    assert booking.id is not None
    logger.info("Тест 2: Модель брони - успешно, id=%s, комната=%s", booking.id, room.id)


def test_3_serializer_valid():
    data = {
        "description": "Хорошее описание номера отеля более 10 символов",
        "price_per_night": 8000.00
    }
    serializer = HotelRoomSerializer(data=data)
    is_valid = serializer.is_valid()
    if is_valid:
        logger.info("Тест 3: Сериализатор валидный - успешно")
    else:
        logger.error("Тест 3: Сериализатор невалидный - ошибки: %s", serializer.errors)
    assert is_valid


@pytest.mark.django_db
def test_4_api_create_room():
    client = APIClient()
    data = {
        "description": "API номер с описанием более 10 символов",
        "price_per_night": 9000.00
    }
    response = client.post('/rooms/', data, format='json')
    log_response("Тест 4: API создание номера", response, key='id')
    assert response.status_code == 201


@pytest.mark.django_db
def test_5_api_create_booking():
    client = APIClient()
    room = HotelRoom.objects.create(
        description="Номер для тестирования бронирования API",
        price_per_night=6000.00
    )
    future = (timezone.now() + timedelta(days=30)).date()
    data = {
        "room_id": room.id,
        "date_start": str(future),
        "date_end": str(future + timedelta(days=2))
    }
    response = client.post('/bookings/create/', data, format='json')
    log_response("Тест 5: Создание брони", response, key='booking_id')
    assert response.status_code == 201
    assert 'booking_id' in response.data


@pytest.mark.django_db
def test_6_api_get_rooms():
    client = APIClient()
    room = HotelRoom.objects.create(
        description="Тестовый номер для списка",
        price_per_night=4000.00
    )
    response = client.get('/rooms/')
    if response.status_code == 200:
        count = len(response.data.get('results', []))
        logger.info("Тест 6: API получение списка номеров - успешно, количество=%s, id=%s", count, room.id)
    else:
        logger.error("Тест 6: API получение списка номеров - ошибка, ответ=%s", response.data)
    assert response.status_code == 200
    assert 'results' in response.data


@pytest.mark.django_db
def test_7_api_get_room_bookings():
    client = APIClient()
    room = HotelRoom.objects.create(
        description="Номер для получения броней",
        price_per_night=5500.00
    )
    booking = Booking.objects.create(
        room=room,
        date_start=date(2025, 9, 1),
        date_end=date(2025, 9, 5)
    )
    response = client.get(f'/bookings/list/?room_id={room.id}')
    if response.status_code == 200:
        count = len(response.data.get('results', []))
        logger.info("Тест 7: API бронирования - успешно, количество=%s, комната=%s, бронь=%s", count, room.id, booking.id)
    else:
        logger.error("Тест 7: API бронирования - ошибка, ответ=%s", response.data)
    assert response.status_code == 200
    assert len(response.data.get('results', [])) == 1


@pytest.mark.django_db
def test_8_api_create_booking_overlap():
    client = APIClient()
    room = HotelRoom.objects.create(
        description="Номер для теста пересечения броней",
        price_per_night=7000.00
    )
    Booking.objects.create(room=room, date_start=date(2025, 10, 1), date_end=date(2025, 10, 5))
    data_overlap = {"room_id": room.id, "date_start": "2025-10-04", "date_end": "2025-10-08"}
    response = client.post('/bookings/create/', data_overlap, format='json')
    if response.status_code == 400 and "date_start" in response.data:
        logger.info("Тест 8: Попытка брони с пересечением - успешно, ошибка=%s", response.data["date_start"])
    else:
        logger.error("Тест 8: Ошибка теста, ответ=%s", response.data)
    assert response.status_code == 400
    assert "date_start" in response.data


@pytest.mark.django_db
def test_9_api_create_booking_no_overlap():
    client = APIClient()
    room = HotelRoom.objects.create(
        description="Номер для теста пересечений",
        price_per_night=5000.00
    )
    existing_start = (timezone.now() + timedelta(days=30)).date()
    existing_end = existing_start + timedelta(days=5)
    Booking.objects.create(room=room, date_start=existing_start, date_end=existing_end)
    data_before = {
        "room_id": room.id,
        "date_start": str(existing_start - timedelta(days=6)),
        "date_end": str(existing_start - timedelta(days=1))
    }
    data_after = {
        "room_id": room.id,
        "date_start": str(existing_end + timedelta(days=1)),
        "date_end": str(existing_end + timedelta(days=5))
    }
    response_before = client.post('/bookings/create/', data_before, format='json')
    response_after = client.post('/bookings/create/', data_after, format='json')
    log_response("Тест 9a: Бронь до существующей", response_before, key=None)
    log_response("Тест 9b: Бронь после существующей", response_after, key=None)
    assert response_before.status_code == 201, f"Ошибка: {response_before.data}"
    assert response_after.status_code == 201, f"Ошибка: {response_after.data}"


@pytest.mark.django_db
def test_10_api_create_booking_end_before_start():
    client = APIClient()
    room = HotelRoom.objects.create(
        description="Номер для проверки date_end < date_start",
        price_per_night=5000.00
    )
    data = {"room_id": room.id, "date_start": "2025-12-10", "date_end": "2025-12-05"}
    response = client.post('/bookings/create/', data, format='json')
    if response.status_code == 400 and "date_end" in response.data:
        logger.info("Тест 10: date_end < date_start - успешно, ошибка=%s", response.data["date_end"])
    else:
        logger.error("Тест 10: Ошибка теста, ответ=%s", response.data)
    assert response.status_code == 400
    assert "date_end" in response.data


@pytest.mark.django_db
def test_11_api_create_booking_in_past():
    client = APIClient()
    room = HotelRoom.objects.create(
        description="Номер для проверки прошлой даты",
        price_per_night=5000.00
    )
    past_date = (timezone.now() - timedelta(days=10)).date()
    data = {"room_id": room.id, "date_start": str(past_date), "date_end": str(past_date + timedelta(days=2))}
    response = client.post('/bookings/create/', data, format='json')
    if response.status_code == 400 and "date_start" in response.data:
        logger.info("Тест 11: Попытка брони в прошлом - успешно, ошибка=%s", response.data["date_start"])
    else:
        logger.error("Тест 11: Ошибка теста, ответ=%s", response.data)
    assert response.status_code == 400
    assert "date_start" in response.data


@pytest.mark.django_db
def test_12_api_create_booking_nonexistent_room():
    client = APIClient()
    data = {"room_id": 9999, "date_start": "2025-12-01", "date_end": "2025-12-05"}
    response = client.post('/bookings/create/', data, format='json')
    log_response("Тест 12: Несуществующая комната", response, success_status=400, key="room_id")
    assert response.status_code == 400
    assert "room_id" in response.data
    assert response.data["room_id"] == ["Room not found"]


@pytest.mark.django_db
def test_13_api_delete_nonexistent_booking():
    client = APIClient()
    response = client.delete('/bookings/99999/delete/')
    log_response("Тест 13: Удаление несуществующей брони", response, success_status=404)
    assert response.status_code == 404


@pytest.mark.django_db
def test_14_api_delete_nonexistent_room():
    client = APIClient()
    response = client.delete('/rooms/99999/')
    log_response("Тест 14: Удаление несуществующего номера", response, success_status=404)
    assert response.status_code == 404
