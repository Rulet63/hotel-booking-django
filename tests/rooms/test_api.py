import pytest
import json
from rest_framework.test import APIClient
from rooms.models import HotelRoom


@pytest.mark.django_db
class TestHotelRoomAPI:
    
    def setup_method(self):
        self.client = APIClient()
        
    def test_create_room_success(self):
        """Тест успешного создания номера через API."""
        data = {
            "description": "Тестовый номер через API с описанием более 10 символов",
            "price_per_night": 8500.00
        }
        
        response = self.client.post(
            '/api/rooms/',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        assert response.status_code == 201
        assert response.data['description'] == data['description']
        assert float(response.data['price_per_night']) == data['price_per_night']
        print(f"✓ API: Создан номер ID: {response.data['id']}")
        
    def test_create_room_validation_error_short_description(self):
        """Тест валидации слишком короткого описания."""
        data = {"description": "Коротко", "price_per_night": 5000}
        
        response = self.client.post(
            '/api/rooms/',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        assert 'error' in response.data
        print("✓ API: Валидация короткого описания работает")
        
    def test_create_room_validation_error_negative_price(self):
        """Тест валидации отрицательной цены."""
        data = {"description": "Нормальное описание", "price_per_night": -100}
        
        response = self.client.post(
            '/api/rooms/',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        assert 'error' in response.data
        print("✓ API: Валидация отрицательной цены работает")
        
    def test_get_rooms_list(self):
        """Тест получения списка номеров."""
        HotelRoom.objects.create(description="Дешевый номер", price_per_night=3000)
        HotelRoom.objects.create(description="Дорогой номер", price_per_night=15000)
        
        response = self.client.get('/api/rooms/')
        
        assert response.status_code == 200
        assert 'results' in response.data
        assert response.data['count'] == 2
        print("✓ API: Получено {response.data['count']} номеров")
        
    def test_room_sorting_by_price_asc(self):
        """Тест сортировки номеров по цене (возрастание)."""
        HotelRoom.objects.create(description="Средний", price_per_night=8000)
        HotelRoom.objects.create(description="Дешевый", price_per_night=3000)
        HotelRoom.objects.create(description="Дорогой", price_per_night=12000)
        
        response = self.client.get('/api/rooms/?ordering=price_per_night')
        
        assert response.status_code == 200
        prices = [float(room['price_per_night']) for room in response.data['results']]
        assert prices == sorted(prices)
        print("✓ API: Сортировка по возрастанию цены работает")
        
    def test_room_sorting_by_price_desc(self):
        """Тест сортировки номеров по цене (убывание)."""
        HotelRoom.objects.create(description="Средний", price_per_night=8000)
        HotelRoom.objects.create(description="Дешевый", price_per_night=3000)
        
        response = self.client.get('/api/rooms/?ordering=-price_per_night')
        
        assert response.status_code == 200
        prices = [float(room['price_per_night']) for room in response.data['results']]
        assert prices == sorted(prices, reverse=True)
        print("✓ API: Сортировка по убыванию цены работает")
        
    def test_delete_room(self):
        """Тест удаления номера."""
        room = HotelRoom.objects.create(
            description="Номер для удаления",
            price_per_night=6000
        )
        
        response = self.client.delete(f'/api/rooms/{room.id}/')
        
        assert response.status_code == 204
        # Проверяем что номер удалился
        assert not HotelRoom.objects.filter(id=room.id).exists()
        print(f"✓ API: Номер ID:{room.id} успешно удален")
        
    def test_delete_nonexistent_room(self):
        """Тест удаления несуществующего номера."""
        response = self.client.delete('/api/rooms/999999/')
        
        assert response.status_code == 404
        print("✓ API: Удаление несуществующего номера возвращает 404")
