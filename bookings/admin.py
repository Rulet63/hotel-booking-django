from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'room', 'date_start', 'date_end', 'created_at')
    list_filter = ('date_start', 'room')
    search_fields = ('room__id',)