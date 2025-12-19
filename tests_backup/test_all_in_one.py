"""
Все основные тесты в одном файле для простоты.
"""
import pytest
import json
from datetime import date, timedelta
from django.utils import timezone
from rest_framework.test import APIClient
from rooms.models import HotelRoom
from bookings.models import Booking
from rooms.serializers import HotelRoomSerializer


# ========== ТЕСТ 1: Модели ==========
@pytest.mark.django_db
def test_models_hotelroom_creation():
    """Тест создания модели номера."""
    room = HotelRoom.objects.create(
        description="Тестовый номер",
        price_per_night=5000.00
    )
    assert room.id is not None
    print(f"✓ Модель: Создан номер ID {room.id}")


@pytest.mark.django_db  
def test_models_booking_creation():
    """Тест создания модели брони."""
    room = HotelRoom.objects.create(
        description="Номер для брони",
        price_per_night=7000.00
    )
    booking = Booking.objects.create(
        room=room,
        date_start=date(2025, 6, 20),
        date_end=date(2025, 6, 25)
    )
    assert booking.id is not None
    print(f"✓ Модель: Создана бронь ID {booking.id}")


# ========== ТЕСТ 2: Сериализаторы ==========
def test_serializers_valid():
    """Тест валидного сериализатора."""
    data = {"description": "Хорошее описание", "price_per_night": 8000}
    serializer = HotelRoomSerializer(data=data)
    assert serializer.is_valid() is True
    print("✓ Сериализатор: Валидные данные проходят")


def test_serializers_invalid_price():
    """Тест невалидной цены."""
    data = {"description": "Номер", "price_per_night": -100}
    serializer = HotelRoomSerializer(data=data)
    assert serializer.is_valid() is False
    print("✓ Сериализатор: Отрицательная цена отклоняется")


# ========== ТЕСТ 3: API Номера ==========
@pytest.mark.django_db
class TestAPIRooms:
    
    def setup_method(self):
        self.client = APIClient()
        
    def test_api_create_room(self):
        """Тест создания номера через API."""
        data = {
            "description": "Номер созданный через API тест",
            "price_per_night": 9500.00
        }
        response = self.client.post('/api/rooms/', data, format='json')
        assert response.status_code == 201
        print(f"✓ API Номера: Создан номер ID {response.data.get('id')}")
        
    def test_api_get_rooms(self):
        """Тест получения списка номеров."""
        HotelRoom.objects.create(description="Тест номер", price_per_night=4000)
        response = self.client.get('/api/rooms/')
        assert response.status_code == 200
        print(f"✓ API Номера: Получено {response.data.get('count', 0)} номеров")


# ========== ТЕСТ 4: API Бронирования ==========
@pytest.mark.django_db
class TestAPIBookings:
    
    def setup_method(self):
        self.client = APIClient()
        self.room = HotelRoom.objects.create(
            description="Номер для теста броней",
            price_per_night=6500.00
        )
        
    def test_api_create_booking(self):
        """Тест создания брони через API."""
        future = (timezone.now() + timedelta(days=30)).date()
        data = {
            "room_id": self.room.id,
            "date_start": str(future),
            "date_end": str(future + timedelta(days=3))
        }
        response = self.client.post('/api/bookings/', data, format='json')
        assert response.status_code == 200
        print(f"✓ API Брони: Создана бронь ID {response.data.get('booking_id')}")
        
    def test_api_get_room_bookings(self):
        """Тест получения броней номера."""
        Booking.objects.create(
            room=self.room,
            date_start=date(2025, 9, 1),
            date_end=date(2025, 9, 5)
        )
        response = self.client.get(f'/api/rooms/{self.room.id}/bookings/')
        assert response.status_code == 200
        print(f"✓ API Брони: Получено {len(response.data)} броней")
