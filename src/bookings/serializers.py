from rest_framework import serializers
from .models import Booking


class BookingSerializer(serializers.ModelSerializer):
    
    room_id = serializers.IntegerField(write_only=True)
    booking_id = serializers.IntegerField(source='id', read_only=True)
    
    class Meta:
        model = Booking
        fields = ['booking_id', 'date_start', 'date_end', 'room_id']
        read_only_fields = ['booking_id']
        
    def validate(self, data):
        # Проверяем что дата начала <= дата окончания
        if 'date_start' in data and 'date_end' in data:
            if data['date_start'] > data['date_end']:
                raise serializers.ValidationError({
                    'date_end': 'Дата окончания должна быть после даты начала'
                })
        return data
    
    def create(self, validated_data):
        from rooms.models import HotelRoom
        
        room_id = validated_data.pop('room_id')
        try:
            room = HotelRoom.objects.get(id=room_id)
        except HotelRoom.DoesNotExist:
            raise serializers.ValidationError({'room_id': 'Room not found'})
        
        validated_data['room'] = room
        return super().create(validated_data)


class BookingListSerializer(serializers.ModelSerializer):
    booking_id = serializers.IntegerField(source='id')
    
    class Meta:
        model = Booking
        fields = ['booking_id', 'date_start', 'date_end']
