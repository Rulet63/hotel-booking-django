import logging
from datetime import date, timedelta

import pytest
from django.utils import timezone
from rest_framework.test import APIClient

from bookings.models import Booking
from rooms.models import HotelRoom
from rooms.serializers import HotelRoomSerializer


logger = logging.getLogger(__name__)

@pytest.mark.django_db
def test_1_model_room():
    """Тест создания модели номера отеля."""
    room = HotelRoom.objects.create(
        description="Тестовый номер отеля с описанием",
        price_per_night=5000.00
    )
    assert room.id is not None
    logger.info("Тест 1: Модель номера - успешно создана, id=%s", room.id)


@pytest.mark.django_db
def test_2_model_booking():
    """Тест создания модели бронирования."""
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
    logger.info(
        "Тест 2: Модель брони - успешно создана, id=%s, комната=%s",
        booking.id, room.id
    )


def test_3_serializer_valid():
    """Тест валидации сериализатора."""
    data = {
        "description": "Хорошее описание номера отеля более 10 символов",
        "price_per_night": 8000.00
    }
    serializer = HotelRoomSerializer(data=data)
    is_valid = serializer.is_valid()

    if is_valid:
        logger.info("Тест 3: Сериализатор валидный - успешно")
    else:
        logger.error(
            "Тест 3: Сериализатор невалидный - ошибки: %s",
            serializer.errors
        )

    assert is_valid is True


@pytest.mark.django_db
def test_4_api_create_room():
    """Тест API создания номера отеля."""
    client = APIClient()
    data = {
        "description": "API номер с описанием более 10 символов",
        "price_per_night": 9000.00
    }
    response = client.post('/rooms/', data, format='json')

    if response.status_code == 201:
        room_id = response.data.get('id')
        logger.info(
            "Тест 4: API создание номера - успешно, статус=%s, id=%s",
            response.status_code, room_id
        )
    else:
        logger.error(
            "Тест 4: API создание номера - ошибка, статус=%s, ответ=%s",
            response.status_code, response.data
        )

    assert response.status_code == 201


@pytest.mark.django_db
def test_5_api_create_booking():
    """Тест API создания бронирования."""
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

    if response.status_code == 201:
        booking_id = response.data.get('booking_id')
        logger.info(
            "Тест 5: API создание брони - успешно, статус=%s, id=%s, комната=%s",
            response.status_code, booking_id, room.id
        )
    else:
        logger.error(
            "Тест 5: API создание брони - ошибка, статус=%s, ответ=%s",
            response.status_code, response.data
        )

    assert response.status_code == 201
    assert 'booking_id' in response.data


@pytest.mark.django_db
def test_6_api_get_rooms():
    """Тест API получения списка номеров."""
    client = APIClient()
    room = HotelRoom.objects.create(
        description="Тестовый номер для списка",
        price_per_night=4000.00
    )
    response = client.get('/rooms/')

    if response.status_code == 200:
        count = len(response.data.get('results', []))
        logger.info(
            "Тест 6: API получение списка номеров - успешно, "
            "статус=%s, количество=%s, созданный id=%s",
            response.status_code, count, room.id
        )
    else:
        logger.error(
            "Тест 6: API получение списка номеров - ошибка, статус=%s, ответ=%s",
            response.status_code, response.data
        )

    assert response.status_code == 200
    assert 'results' in response.data


@pytest.mark.django_db
def test_7_api_get_room_bookings():
    """Тест API получения бронирований номера."""
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
        if isinstance(response.data, dict) and 'results' in response.data:
            count = len(response.data['results'])
        else:
            count = len(response.data)

        logger.info(
            "Тест 7: API получение бронирований номера - успешно, "
            "статус=%s, количество бронирований=%s, комната=%s, бронь=%s",
            response.status_code, count, room.id, booking.id
        )
    else:
        logger.error(
            "Тест 7: API получение бронирований номера - ошибка, "
            "статус=%s, ответ=%s",
            response.status_code, response.data
        )

    assert response.status_code == 200

    if isinstance(response.data, dict) and 'results' in response.data:
        assert len(response.data['results']) == 1
    else:
        assert len(response.data) == 1

