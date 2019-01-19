from django.contrib.auth.models import User
from rest_framework import serializers
from .models import LyfteeSchedule
from .models import LyfterService
from .models import PoolRide


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ('password', )


class LyfteeScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = LyfteeSchedule
        fields = "__all__"

    is_allocated = serializers.SerializerMethodField()
    user_details = serializers.SerializerMethodField()

    def get_is_allocated(self, obj):
        return obj.is_allocated

    def get_user_details(self, obj):
        user = User.objects.get(id=obj.user.id)
        return UserSerializer(user).data


class LyfterServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = LyfterService
        fields = "__all__"


class PoolRideSerializer(serializers.ModelSerializer):

    lyftee_schedule = LyfteeScheduleSerializer(read_only=True)
    lyfter_service = LyfterServiceSerializer(read_only=True)

    class Meta:
        model = PoolRide
        fields = "__all__"





