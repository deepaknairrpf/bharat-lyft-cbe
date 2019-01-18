from django.contrib.auth.models import User
from rest_framework import serializers
from .models import LyfteeSchedule
from .models import LyfterService


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class LyfteeScheduleSerializer(serializers.ModelSerializer):

    user = UserSerializer(read_only=True)

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


