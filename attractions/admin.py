from django.contrib import admin
from .models import Attraction

# Register your models here.
@admin.register(Attraction)
class AttractionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'destination', 'created_at', 'updated_at')