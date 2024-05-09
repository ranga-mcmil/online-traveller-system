from django.contrib import admin
from .models import Flight, FlightRoute, GeneratedRoute

# Register your models here.
@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ('id', 'airline', 'price', 'created_at', 'updated_at')

@admin.register(FlightRoute)
class FlightPathAdmin(admin.ModelAdmin):
    list_display = ('id', 'flight', 'destination', 'departure', 'arrival')


@admin.register(GeneratedRoute)
class GeneratedRouteAdmin(admin.ModelAdmin):
    list_display = ('id',)