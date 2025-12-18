from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from .models import Booking
from rooms.models import HotelRoom
from .serializers import BookingSerializer


class BookingViewSet(viewsets.ModelViewSet):
    """
    API endpoint для управления бронированиями.
    POST /api/bookings/ - создать бронь
    DELETE /api/bookings/{id}/ - удалить бронь
    """
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [AllowAny]  # По ТЗ - без авторизации
    
    def get_serializer_context(self):
        """Добавляем request в контекст для сериализатора"""
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
    def list(self, request):
        """Отключаем общий список бронирований (не требуется по ТЗ)"""
        return Response(
            {"detail": "Используйте GET /api/rooms/{id}/bookings/ для получения списка броней"},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )


class RoomBookingsViewSet(viewsets.ViewSet):
    """
    API endpoint для получения списка броней конкретного номера.
    GET /api/rooms/{id}/bookings/
    """
    permission_classes = [AllowAny]
    
    def list(self, request, room_id=None):
        """Список бронирований для конкретного номера"""
        room = get_object_or_404(HotelRoom, id=room_id)
        bookings = Booking.objects.filter(room=room).order_by('date_start')
        
        serializer = BookingSerializer(bookings, many=True, context={'request': request})
        return Response(serializer.data)