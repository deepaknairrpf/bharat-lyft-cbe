from rest_framework import serializers
from .models import LyfteeSchedule

class LyfteeScheduleSerializer(serializers.ModelSerializer):

    class Meta:
        model = LyfteeSchedule
        exclude = ('is_allocated',)
