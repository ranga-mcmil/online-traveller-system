from django.contrib import admin
from .models import Destination

# Register your models here.
@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'country', 'created_at', 'updated_at')