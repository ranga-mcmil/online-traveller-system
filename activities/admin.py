from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Activity, ActivityBooking

# Register your models here.
@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'destination', 'category', 'price', 'image', 'created_at', 'updated_at')

@admin.register(ActivityBooking)
class ActivityBookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'activity', 'date', 'people', 'created_at', 'updated_at')