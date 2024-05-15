from django.contrib import admin
from .models import AccommodationReview

@admin.register(AccommodationReview)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'content',  'created_at')
