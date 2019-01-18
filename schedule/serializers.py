from django.contrib.auth.models import User
from rest_framework import serializers
from .models import LyfteeSchedule
from .models import LyfterService
from .models import PoolRide


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class LyfteeScheduleSerializer(serializers.ModelSerializer):

    user = serializers.PrimaryKeyRelatedField(many=False, read_only=True)

    class Meta:
        model = LyfteeSchedule
        fields = "__all__"

    is_allocated = serializers.SerializerMethodField()


    def get_is_allocated(self, obj):
        return obj.is_allocated


class LyfterServiceSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    class Meta:
        model = LyfterService
        fields = "__all__"


class PoolRideSerializer(serializers.ModelSerializer):

    lyftee_schedule = serializers.PrimaryKeyRelatedField(many=False)
    lyfter_service = serializers.PrimaryKeyRelatedField(many=False)

    class Meta:
        model = PoolRide
        fields = "__all__"




