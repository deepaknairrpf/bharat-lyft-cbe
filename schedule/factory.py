import datetime
from datetime import timedelta
from factory import Iterator, SubFactory, PostGenerationMethodCall
from factory.django import DjangoModelFactory
from django.contrib.auth.models import User
from factory.fuzzy import FuzzyText

from .models import LyfteeSchedule
from .models import LyfterService
from .models import PoolRide



class UserFactory(DjangoModelFactory):

    class Meta:
        model = User

    username = FuzzyText()
    first_name = FuzzyText()
    password = PostGenerationMethodCall(
        'set_password', 'defaultPassword123'
    )
    is_staff = True


class LyfteeScheduleFactory(DjangoModelFactory):

    source_lat = 13.090104
    source_long = 80.205357
    destination_lat = 13.086637
    destination_long = 80.217377
    scheduled_time = datetime.datetime.now()
    user = SubFactory(UserFactory)
    timestamp = datetime.datetime.now() - timedelta(days=1)

    class Meta:
        model = LyfteeSchedule

class LyfterServiceFactory(DjangoModelFactory):

    user = SubFactory(UserFactory)
    source_lat = 23.142
    source_long = 21.242
    destination_lat = 21.512
    destination_long = 11.24

    class Meta:
        model = LyfterService


class PoolRideFactory(DjangoModelFactory):
    lyftee_schedule = SubFactory(LyfteeScheduleFactory)
    lyfter_service = SubFactory(LyfterServiceFactory)
    pickup_point_lat = 21.412
    pickup_point_long = 25.125
    timestamp = datetime.datetime.now()

    class Meta:
        model = PoolRide

