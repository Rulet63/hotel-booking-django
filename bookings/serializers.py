from rest_framework import serializers
from .models import Booking
from rooms.models import HotelRoom


class BookingSerializer(serializers.ModelSerializer):
    room_id = serializers.PrimaryKeyRelatedField(
        queryset=HotelRoom.objects.all(),
        source='room',
        write_only=True
    )
    
    class Meta:
        model = Booking
        fields = ['id', 'room_id', 'date_start', 'date_end', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def validate(self, data):
        """
        Валидация дат:
        1. date_end должен быть >= date_start
        2. Даты должны быть валидными (автоматически проверяется DateField)
        """
        if data['date_start'] > data['date_end']:
            raise serializers.ValidationError({
                "date_end": "Дата окончания должна быть позже или равна дате начала"
            })
        
        # Дополнительная валидация (можно добавить проверку на пересечение бронирований)
        # room = data['room']
        # existing_bookings = Booking.objects.filter(
        #     room=room,
        #     date_start__lt=data['date_end'],
        #     date_end__gt=data['date_start']
        # )
        # if existing_bookings.exists():
        #     raise serializers.ValidationError("Номер уже забронирован на эти даты")
        
        return data
    
    def to_representation(self, instance):
        """
        Изменяем формат ответа согласно ТЗ:
        При создании возвращаем {"booking_id": id}
        При получении списка возвращаем полные данные
        """
        representation = super().to_representation(instance)
        
        
        if self.context.get('request') and self.context['request'].method == 'POST':
            return {"booking_id": representation['id']}
        
        
        return representation