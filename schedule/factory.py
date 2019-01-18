import datetime
from datetime import timedelta
from factory import Iterator, SubFactory, PostGenerationMethodCall
from factory.django import DjangoModelFactory
from django.contrib.auth.models import User
from factory.fuzzy import FuzzyText

from .models import LyfteeSchedule



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