from django.contrib import admin
from .models import HotelRoom

@admin.register(HotelRoom)
class HotelRoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'price_per_night', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('description',)
