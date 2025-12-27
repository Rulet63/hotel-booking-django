from django.contrib import admin

from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("id", "room_id", "date_start", "date_end", "created_at", "is_active")
    list_filter = ("date_start", "date_end", "room")
    search_fields = ("room__id",)
    list_select_related = True  
    date_hierarchy = "date_start" 
    
    def is_active(self, obj):
        """Показываем, активно ли бронирование сейчас."""
        from django.utils import timezone
        today = timezone.now().date()
        return obj.date_start <= today <= obj.date_end
    is_active.boolean = True
    is_active.short_description = "Active"
    