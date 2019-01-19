import datetime

import googlemaps
import pytz
from dateutil import parser
from django.utils import timezone
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from lyft.settings import GMAPS_API_KEY
from schedule.factory import LyfteeScheduleFactory
from schedule.functions.internal import SchedulerEngine
from schedule.models import PoolRide
from .models import LyfteeSchedule
from .models import LyfterService
from .serializers import LyfteeScheduleSerializer
from .serializers import LyfterServiceSerializer
from .serializers import PoolRideSerializer


class LyfteeScheduleViewset(viewsets.ModelViewSet):
    queryset = LyfteeSchedule.objects.all()
    serializer_class = LyfteeScheduleSerializer

    def create(self, request, *args, **kwargs):

        def displace_time_in_utc_to_reflect_target_timezone(target_timezone, target_time):
            """Displaces time in UTC that matches the time in target timezone.

                Args:
                target_timezone (str): One the of the supported timezone strings.
                target_time (datetime.datetime): Input time that has to be displaced.

                Returns:
                The time is displaced in UTC to reflect the time in target timezone.
                """
            time_in_target_timezone = target_time.replace(
                tzinfo=pytz.timezone(target_timezone)
            )
            print(time_in_target_timezone)
            return time_in_target_timezone.astimezone(pytz.utc)

        user =request.user
        request_data = request.data.copy()
        request_data["user"] = user.id
        tz = pytz.timezone("Asia/Calcutta")
        indian_time = tz.localize(parser.parse(request_data["scheduled_time"]))
        scheduled_time = indian_time.astimezone(pytz.utc)
        request_data["scheduled_time"] = scheduled_time
        serializer = LyfteeScheduleSerializer(data=request_data)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LyfterServiceViewset(viewsets.ModelViewSet):
    queryset = LyfterService.objects.all()
    serializer_class = LyfterServiceSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        request_data = request.data.copy()
        request_data["user"] = user.id
        serializer = LyfterServiceSerializer(data=request_data)
        print("data", request_data)
        if serializer.is_valid():
            object = serializer.save()
            return Response(data=LyfterServiceSerializer(object).data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=True,
        url_path = "find-lyftee",
        url_name = "find-lyftee",
        methods=['get']
    )
    def find_lyftee(self, request, *args, **kwargs):
        lyfter_service_object = self.get_object()
        google_client = googlemaps.Client(key=GMAPS_API_KEY)
        engine = SchedulerEngine(lyfter_service_object, google_client)
        candidate_lyftee_point = engine.suggest_lyftee()
        if candidate_lyftee_point:
            pool_ride_object = PoolRide.objects.create(
                lyfter_service=lyfter_service_object,
                lyftee_schedule=candidate_lyftee_point.lyftee_schedule_obj,
                pickup_point_lat=candidate_lyftee_point.src_nearest_point[0],
                pickup_point_long=candidate_lyftee_point.src_nearest_point[1],
                drop_point_lat=candidate_lyftee_point.dest_nearest_point[0],
                drop_point_long=candidate_lyftee_point.dest_nearest_point[1],
                timestamp=datetime.datetime.now()
            )
            serializer = PoolRideSerializer(pool_ride_object)
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        return Response(data=None, status=status.HTTP_200_OK)


class PoolRideViewset(viewsets.ModelViewSet):
    queryset = PoolRide.objects.all()
    serializer_class = PoolRideSerializer

    @action(
        detail=False,
        url_path = "get-latest-assigned-ride",
        url_name = "get-latest-assigned-ride",
        methods=['get']
    )
    def get_latest_assigned_ride(self, request, *args, **kwargs):
        user = request.user
        recently_assigned_pool_rides = PoolRide.objects.filter(
            lyftee_schedule__user=user.id,
            has_ride_completed=False
        ).order_by('-timestamp')
        if len(recently_assigned_pool_rides) > 0:
            serializer = PoolRideSerializer(recently_assigned_pool_rides.first())
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        return Response(data=None, status=status.HTTP_200_OK)
