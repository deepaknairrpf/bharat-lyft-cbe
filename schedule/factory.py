import datetime
from datetime import timedelta
from factory import Iterator
from factory.django import DjangoModelFactory
from django.contrib.auth.models import User
from .models import LyfteeSchedule


class LyfteeScheduleFactory(DjangoModelFactory):

    source_lat = 23.142
    source_long = 21.242
    destination_lat = 21.512
    destination_long = 11.24
    scheduled_time = datetime.datetime.now()
    user = Iterator(User.objects.all())
    timestamp = datetime.datetime.now() - timedelta(days=1)

    class Meta:
        model = LyfteeSchedule