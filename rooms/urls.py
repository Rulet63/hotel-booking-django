from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from bookings.views import RoomBookingsViewSet

router = DefaultRouter()
router.register(r'', views.HotelRoomViewSet, basename='hotelroom')

# Создаем отдельный маршрут для бронирований номера
room_bookings = RoomBookingsViewSet.as_view({'get': 'list'})

urlpatterns = [
    path('', include(router.urls)),
    path('<int:room_id>/bookings/', room_bookings, name='room-bookings'),
]