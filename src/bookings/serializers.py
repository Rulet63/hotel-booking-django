from rest_framework import serializers
from django.utils import timezone
from .models import Booking
from rooms.models import HotelRoom


class BookingSerializer(serializers.ModelSerializer):
    room_id = serializers.IntegerField(write_only=True)
    booking_id = serializers.IntegerField(source="id", read_only=True)

    class Meta:
        model = Booking
        fields = ["booking_id", "date_start", "date_end", "room_id"]
        read_only_fields = ["booking_id"]

    def validate(self, data):
        date_start = data.get("date_start")
        date_end = data.get("date_end")
        room_id = data.get("room_id")

        # Проверка обязательного поля room_id
        if not room_id:
            raise serializers.ValidationError({"room_id": "Обязательное поле"})

        # Проверка существования комнаты
        if not HotelRoom.objects.filter(id=room_id).exists():
            raise serializers.ValidationError({"room_id": "Room not found"})

        # Проверка формата и логики дат
        if date_start and date_end:
            if date_start > date_end:
                raise serializers.ValidationError({
                    "date_end": "Дата окончания должна быть после даты начала"
                })

            today = timezone.now().date()
            if date_start < today:
                raise serializers.ValidationError({
                    "date_start": "Нельзя бронировать на прошедшие даты"
                })

            # Проверка пересечения с существующими бронями
            overlapping = Booking.objects.filter(
                room_id=room_id,
                date_start__lte=date_end,
                date_end__gte=date_start
            )
            if self.instance:
                # Исключаем текущую бронь при обновлении
                overlapping = overlapping.exclude(pk=self.instance.pk)
            if overlapping.exists():
                raise serializers.ValidationError({
                    "date_start": "Номер уже забронирован на эти даты"
                })

        return data

    def create(self, validated_data):
        # Получаем объект комнаты
        room = HotelRoom.objects.get(id=validated_data.pop("room_id"))
        validated_data["room"] = room
        return super().create(validated_data)


class BookingListSerializer(serializers.ModelSerializer):
    booking_id = serializers.IntegerField(source="id")

    class Meta:
        model = Booking
        fields = ["booking_id", "date_start", "date_end"]
