from bookings import views as booking_views
from django.contrib import admin
from django.urls import path
from rooms import views as room_views

urlpatterns = [
    path("admin/", admin.site.urls),
    # КОМНАТЫ (по ТЗ)
    path("rooms/", room_views.HotelRoomListView.as_view(), name="room-list"),
    path(
        "rooms/<int:pk>/", room_views.HotelRoomDetailView.as_view(), name="room-detail"
    ),
    # БРОНИРОВАНИЯ (по ТЗ)
    path(
        "bookings/create",
        booking_views.BookingCreateTZView.as_view(),
        name="booking-create",
    ),
    path(
        "bookings/<int:booking_id>/delete",
        booking_views.BookingDeleteTZView.as_view(),
        name="booking-delete",
    ),
    path(
        "bookings/list",
        booking_views.RoomBookingsTZView.as_view(),
        name="bookings-list",
    ),
]
