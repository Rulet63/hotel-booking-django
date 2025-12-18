from rest_framework import viewsets, filters
from .models import HotelRoom
from .serializers import HotelRoomSerializer

class HotelRoomViewSet(viewsets.ModelViewSet):
    
    queryset = HotelRoom.objects.all()
    serializer_class = HotelRoomSerializer
    
    
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['price_per_night', 'created_at']
    ordering = ['-created_at'] 
    
    def perform_destroy(self, instance):
        
        instance.delete()
