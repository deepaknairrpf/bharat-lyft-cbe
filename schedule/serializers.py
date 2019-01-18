from rest_framework import serializers
from .models import LyfteeSchedule

class LyfteeScheduleSerializer(serializers.ModelSerializer):

    class Meta:
        model = LyfteeSchedule
        fields = "__all__"

    is_allocated = serializers.SerializerMethodField()


    def get_is_allocated(self, obj):
        return obj.is_allocated

