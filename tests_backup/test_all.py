"""
Основные тесты проекта (финальная версия).
"""
import pytest
import json
from datetime import date, timedelta
from django.utils import timezone
from rest_framework.test import APIClient
from rooms.models import HotelRoom
from bookings.models import Booking
from rooms.serializers import HotelRoomSerializer


print("=== ЗАПУСК ТЕСТОВ ===")

# Тест 1: Модель номера
@pytest.mark.django_db
def test_1_model_room():
    room = HotelRoom.objects.create(
        description="Тестовый номер отеля с описанием",
        price_per_night=5000.00
    )
    assert room.id is not None
    print("✅ Тест 1: Модель номера - ОК")

# Тест 2: Модель брони  
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
    print("✅ Тест 2: Модель брони - ОК")

# Тест 3: Сериализатор
def test_3_serializer_valid():
    data = {
        "description": "Хорошее описание номера отеля более 10 символов",
        "price_per_night": 8000.00
    }
    serializer = HotelRoomSerializer(data=data)
    assert serializer.is_valid() is True
    print("✅ Тест 3: Сериализатор валидный - ОК")

# Тест 4: API создание номера
@pytest.mark.django_db  
def test_4_api_create_room():
    client = APIClient()
    data = {
        "description": "API номер с описанием более 10 символов",
        "price_per_night": 9000.00
    }
    response = client.post('/api/rooms/', data, format='json')
    # DRF возвращает 201 Created при успешном создании
    assert response.status_code == 201
    print(f"✅ Тест 4: API создание номера - ОК (ID: {response.data.get('id')})")

# Тест 5: API создание брони (ИСПРАВЛЕНО: 201 вместо 200)
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
    response = client.post('/api/bookings/', data, format='json')
    # DRF возвращает 201 Created для успешного POST
    assert response.status_code == 201
    assert 'booking_id' in response.data
    print(f"✅ Тест 5: API создание брони - ОК (ID: {response.data.get('booking_id')})")

# Тест 6: API список номеров (ИСПРАВЛЕНО: временно убираем prefetch_related)
@pytest.mark.django_db
def test_6_api_get_rooms():
    client = APIClient()
    HotelRoom.objects.create(
        description="Тестовый номер для списка",
        price_per_night=4000.00
    )
    response = client.get('/api/rooms/')
    assert response.status_code == 200
    # Пагинация возвращает 'results' и 'count'
    assert 'results' in response.data or isinstance(response.data, list)
    print(f"✅ Тест 6: API получение списка номеров - ОК")

# Тест 7: API брони номера
@pytest.mark.django_db
def test_7_api_get_room_bookings():
    client = APIClient()
    room = HotelRoom.objects.create(
        description="Номер для получения броней",
        price_per_night=5500.00
    )
    Booking.objects.create(
        room=room,
        date_start=date(2025, 9, 1),
        date_end=date(2025, 9, 5)
    )
    response = client.get(f'/api/rooms/{room.id}/bookings/')
    assert response.status_code == 200
    assert len(response.data) == 1
    print(f"✅ Тест 7: API получение броней номера - ОК")

print("=== ВСЕ ТЕСТЫ ЗАВЕРШЕНЫ ===")
