from bookings.models import Booking
from bookings.serializers import BookingListSerializer, BookingSerializer
from rest_framework import generics, status
from rest_framework.response import Response

# from django.shortcuts import get_object_or_404
from .models import HotelRoom
from .serializers import HotelRoomSerializer


class HotelRoomListView(generics.ListCreateAPIView):
    queryset = HotelRoom.objects.all().order_by("-created_at")
    serializer_class = HotelRoomSerializer

    def get_queryset(self):
        queryset = HotelRoom.objects.all()

        ordering = self.request.GET.get("ordering", "")
        if ordering == "price_per_night":
            queryset = queryset.order_by("price_per_night")
        elif ordering == "-price_per_night":
            queryset = queryset.order_by("-price_per_night")
        elif ordering == "created_at":
            queryset = queryset.order_by("created_at")
        elif ordering == "-created_at":
            queryset = queryset.order_by("-created_at")
        else:
            queryset = queryset.order_by("-created_at")

        return queryset

    def get_paginated_response(self, data):
        response = super().get_paginated_response(data)
        response.data["count"] = self.paginator.page.paginator.count
        return response


class HotelRoomDetailView(generics.RetrieveDestroyAPIView):
    queryset = HotelRoom.objects.all()
    serializer_class = HotelRoomSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class RoomBookingsView(generics.ListAPIView):
    serializer_class = BookingListSerializer

    def get_queryset(self):
        room_id = self.kwargs.get("room_id")
        return Booking.objects.filter(room_id=room_id).order_by("date_start")


class BookingCreateTZView(generics.CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def create(self, request, *args, **kwargs):
        if request.content_type == "application/x-www-form-urlencoded":
            data = {
                "room_id": request.POST.get("room_id"),
                "date_start": request.POST.get("date_start"),
                "date_end": request.POST.get("date_end"),
                "guest_name": "Guest",  # ТЗ не требует этих полей
                "guest_email": "guest@example.com",  # ТЗ не требует
            }
            serializer = self.get_serializer(data=data)
        else:
            serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        booking = serializer.save()

        return Response({"booking_id": booking.id}, status=status.HTTP_201_CREATED)


class BookingDeleteTZView(generics.DestroyAPIView):
    queryset = Booking.objects.all()
    lookup_field = "id"
    lookup_url_kwarg = "booking_id"

    def delete(self, request, *args, **kwargs):
        self.destroy(request, *args, **kwargs)
        return Response(status=status.HTTP_204_NO_CONTENT)


class RoomBookingsTZView(generics.ListAPIView):
    serializer_class = BookingListSerializer

    def get_queryset(self):
        room_id = self.request.GET.get("room_id")
        if not room_id:
            return Booking.objects.none()

        try:
            room_id = int(room_id)
        except ValueError:
            return Booking.objects.none()

        return Booking.objects.filter(room_id=room_id).order_by("date_start")
