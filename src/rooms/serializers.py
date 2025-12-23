from rest_framework import serializers

from .models import HotelRoom


class HotelRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelRoom
        fields = ["id", "description", "price_per_night", "created_at"]
        read_only_fields = ["id", "created_at"]

    def validate_price_per_night(self, value):
        """
        Валидация цены за ночь.
        """
        if value <= 0:
            raise serializers.ValidationError("Цена должна быть положительной")
        if value > 1000000:
            raise serializers.ValidationError("Цена не может превышать 1,000,000")
        return value

    def validate_description(self, value):
        """
        Валидация описания.
        """
        if len(value.strip()) < 10:
            raise serializers.ValidationError(
                "Описание должно содержать минимум 10 символов"
            )
        if len(value) > 1000:
            raise serializers.ValidationError(
                "Описание не может превышать 1000 символов"
            )
        return value
