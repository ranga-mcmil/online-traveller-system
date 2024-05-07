from django.contrib import admin
from .models import Accommodation, Room, AccomodationBooking

# Register your models here.
@admin.register(Accommodation)
class AccommodationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'destination', 'star_rating', 'pic', 'created_at', 'updated_at')

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'accommodation', 'room_type')

@admin.register(AccomodationBooking)
class AccomodationBookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'accommodation', 'room', 'start_date', 'end_date', 'created_at')