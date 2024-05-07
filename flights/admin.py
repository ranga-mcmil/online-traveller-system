from django.contrib import admin
from .models import Flight, FlightPath

# Register your models here.
@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ('id', 'airline', 'price', 'created_at', 'updated_at')

@admin.register(FlightPath)
class FlightPathAdmin(admin.ModelAdmin):
    list_display = ('id', 'flight', 'destination', 'departure_date', 'arrival_date')

