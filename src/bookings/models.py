from django.db import models
from rooms.models import HotelRoom


class Booking(models.Model):
    room = models.ForeignKey(HotelRoom, on_delete=models.CASCADE, db_index=True)
    date_start = models.DateField(db_index=True)
    date_end = models.DateField(db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    
    class Meta:
        indexes = [
            
            models.Index(fields=['room', 'date_start', 'date_end'], name='idx_booking_room_dates'),
        ]
        ordering = ['-created_at']

    def __str__(self):
        return f"Booking #{self.id} for Room {self.room_id}"

