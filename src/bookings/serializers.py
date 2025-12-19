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
        2. Проверка на пересечение с существующими бронированиями
        """
        date_start = data['date_start']
        date_end = data['date_end']
        room = data['room']
        
        
        if date_start > date_end:
            raise serializers.ValidationError({
                "date_end": "Дата окончания должна быть позже или равна дате начала"
            })
        
    
        from django.utils import timezone
        if date_start < timezone.now().date():
            raise serializers.ValidationError({
                "date_start": "Дата начала не может быть в прошлом"
            })
        
        
        overlapping_bookings = Booking.objects.filter(
            room=room,
            date_start__lt=date_end,  
            date_end__gt=date_start   
        )
        
        
        if self.instance:
            overlapping_bookings = overlapping_bookings.exclude(id=self.instance.id)
        
        if overlapping_bookings.exists():
            raise serializers.ValidationError({
                "non_field_errors": ["Номер уже забронирован на выбранные даты"]
            })
        
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