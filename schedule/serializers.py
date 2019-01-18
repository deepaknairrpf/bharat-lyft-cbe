from rest_framework import serializers
from .models import LyfteeSchedule
from .models import LyfterService

class LyfteeScheduleSerializer(serializers.ModelSerializer):

    class Meta:
        model = LyfteeSchedule
        fields = "__all__"

    is_allocated = serializers.SerializerMethodField()


    def get_is_allocated(self, obj):
        return obj.is_allocated


class LyfterServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = LyfterService
        fields = "__all__"


