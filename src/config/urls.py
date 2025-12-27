from bookings import views as booking_views
from django.contrib import admin
from django.urls import path
from rooms import views as room_views

urlpatterns = [
    path("admin/", admin.site.urls),

    path("rooms/", room_views.HotelRoomListView.as_view(), name="room-list"),
    path(
        "rooms/<int:pk>/", room_views.HotelRoomDetailView.as_view(), name="room-detail"
    ),

    path(
        "bookings/create/",
        booking_views.BookingCreateView.as_view(),
        name="booking-create",
    ),
    path(
        "bookings/<int:pk>/delete/",
        booking_views.BookingDeleteView.as_view(),
        name="booking-delete",
    ),
   
    path(
        "bookings/list/",
        booking_views.RoomBookingsListView.as_view(),
        name="bookings-list-filter",
    ),
       
]

