from django.db import models
from accommodations.models import Accommodation
from accounts.models import User
from activities.models import Activity

class BaseReview(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True  # Mark this as an abstract base class

class AccommodationReview(BaseReview):
    accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE, related_name="reviews")

class ActivityReview(BaseReview):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name="reviews")





