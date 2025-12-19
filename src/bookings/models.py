from django.db import models
from rooms.models import HotelRoom

class Booking(models.Model):
    room = models.ForeignKey(HotelRoom, on_delete=models.CASCADE)
    date_start = models.DateField()
    date_end = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Booking #{self.id} for Room {self.room_id}"