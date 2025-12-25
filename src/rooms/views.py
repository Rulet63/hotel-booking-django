from rest_framework import generics, filters
from rest_framework.pagination import PageNumberPagination

from .models import HotelRoom
from .serializers import HotelRoomSerializer


class HotelRoomPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class HotelRoomListView(generics.ListCreateAPIView):
    queryset = HotelRoom.objects.all()
    serializer_class = HotelRoomSerializer
    pagination_class = HotelRoomPagination  
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['price_per_night', 'created_at']
    ordering = ['-created_at']


class HotelRoomDetailView(generics.RetrieveDestroyAPIView):
    queryset = HotelRoom.objects.all()
    serializer_class = HotelRoomSerializer
    