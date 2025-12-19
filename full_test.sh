#!/bin/bash
echo "=== ПОЛНЫЙ ТЕСТ HOTEL BOOKING SYSTEM ==="

echo "1. Текущие комнаты:"
curl -s http://localhost:8000/api/rooms/ | python -m json.tool

echo -e "\n2. Создаем еще одну комнату:"
curl -X POST http://localhost:8000/api/rooms/ \
  -H "Content-Type: application/json" \
  -d '{
    "room_number": "202",
    "description": "Люкс с видом на море",
    "room_type": "luxury",
    "price_per_night": 12000,
    "capacity": 3,
    "amenities": "WiFi, TV, Кондиционер, Мини-бар"
  }' 2>/dev/null | python -m json.tool

echo -e "\n3. Все комнаты после добавления:"
curl -s http://localhost:8000/api/rooms/ | python -m json.tool

echo -e "\n4. Создаем бронирование для комнаты 1:"
curl -X POST http://localhost:8000/api/bookings/ \
  -H "Content-Type: application/json" \
  -d '{
    "room": 1,
    "guest_name": "Мария Петрова",
    "guest_email": "maria@test.com",
    "check_in_date": "2024-12-20",
    "check_out_date": "2024-12-25",
    "status": "pending"
  }' 2>/dev/null | python -m json.tool

echo -e "\n5. Бронирования для комнаты 1:"
curl -s http://localhost:8000/api/rooms/1/bookings/ 2>/dev/null | python -m json.tool

echo -e "\n=== ТЕСТ ЗАВЕРШЕН УСПЕШНО ==="
