from rest_framework import viewsets, filters
from .models import HotelRoom
from .serializers import HotelRoomSerializer

class HotelRoomViewSet(viewsets.ModelViewSet):
    """
    API endpoint для управления номерами отеля.
    GET /api/rooms/ - список номеров
    POST /api/rooms/ - создать номер
    DELETE /api/rooms/{id}/ - удалить номер
    """
    queryset = HotelRoom.objects.all()  # Убрали prefetch_related для простоты
    serializer_class = HotelRoomSerializer
    
    # Включаем сортировку по цене и дате создания
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['price_per_night', 'created_at']
    ordering = ['-created_at']
    
    def perform_destroy(self, instance):
        """
        При удалении номера автоматически удалятся все его брони
        (каскадное удаление настроено в модели Booking)
        """
        instance.delete()
