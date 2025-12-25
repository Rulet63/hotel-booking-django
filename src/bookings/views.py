from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404

from .models import Booking
from rooms.models import HotelRoom
from .serializers import BookingListSerializer, BookingSerializer


class CustomBookingPagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = 'limit'
    max_page_size = 50
    
    def get_paginated_response(self, data):
        return Response({
            'page': {
                'current': self.page.number,
                'total': self.page.paginator.num_pages,
                'size': len(data),
            },
            'total_count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })


class BookingCreateView(generics.CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        booking = serializer.save()
        
        return Response(
            {"booking_id": booking.id},
            status=status.HTTP_201_CREATED
        )


class BookingDeleteView(generics.DestroyAPIView):
    queryset = Booking.objects.all()


class RoomBookingsListView(generics.ListAPIView):
    serializer_class = BookingListSerializer
    pagination_class = CustomBookingPagination
    
    def get_queryset(self):
        room_id = self.request.query_params.get("room_id")
        
        if not room_id:
            return Booking.objects.all().select_related('room').order_by("date_start")
        
        
        get_object_or_404(HotelRoom, id=room_id)
        
        
        return Booking.objects.filter(
            room_id=room_id
        ).select_related('room').order_by("date_start")