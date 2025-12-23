from rest_framework import generics, status
from rest_framework.response import Response

from .models import Booking
from .serializers import BookingListSerializer, BookingSerializer


class BookingCreateTZView(generics.CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def create(self, request, *args, **kwargs):
        if request.content_type == "application/x-www-form-urlencoded":
            data = {
                "room_id": request.POST.get("room_id"),
                "date_start": request.POST.get("date_start"),
                "date_end": request.POST.get("date_end"),
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
    # pagination_class = None

    def get_queryset(self):
        room_id = self.request.GET.get("room_id")
        if not room_id:
            return Booking.objects.none()

        try:
            room_id = int(room_id)
        except ValueError:
            return Booking.objects.none()

        return Booking.objects.filter(room_id=room_id).order_by("date_start")
