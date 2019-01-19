from django.db import models
from django.contrib.auth.models import User
from utils.model import IntegerRangeField

# Create your models here.

class LyfteeSchedule(models.Model):
    source_lat = models.FloatField()
    source_long = models.FloatField()
    destination_lat = models.FloatField()
    destination_long = models.FloatField()
    scheduled_time = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_allocated = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_valid = models.BooleanField(default=True)

class LyfterService(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    source_lat = models.FloatField()
    source_long = models.FloatField()
    destination_lat = models.FloatField()
    destination_long = models.FloatField()
    lyftee_max_limit = models.PositiveIntegerField(default=1)


class PoolRide(models.Model):
    lyftee_schedule = models.ForeignKey(LyfteeSchedule, on_delete=models.CASCADE)
    lyfter_service = models.ForeignKey(LyfterService, on_delete=models.CASCADE)
    has_ride_completed = models.BooleanField(default=False)
    lyftee_rating = IntegerRangeField(min_value=1, max_value=5, null=True)
    lyfter_rating = IntegerRangeField(min_value=1, max_value=5, null=True)
    pickup_point_lat = models.FloatField()
    pickup_point_long = models.FloatField()
    drop_point_lat = models.FloatField()
    drop_point_long = models.FloatField()
    timestamp = models.DateTimeField()

    class Meta:
        unique_together = ("lyftee_schedule", "lyfter_service")




