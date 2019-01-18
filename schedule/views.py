from rest_framework import viewsets
import datetime
from schedule.factory import LyfteeScheduleFactory
from .models import LyfteeSchedule
from .models import LyfterService
from .serializers import LyfteeScheduleSerializer
from .serializers import LyfterServiceSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from schedule.functions.internal import SchedulerEngine
import googlemaps
from lyft.settings import GMAPS_API_KEY
from schedule.models import PoolRide


class LyfteeScheduleViewset(viewsets.ModelViewSet):
    queryset = LyfteeSchedule.objects.all()
    serializer_class = LyfteeScheduleSerializer

    def create(self, request, *args, **kwargs):
        user =request.user
        request_data = request.POST.copy()
        request_data["user"] = user.id
        serializer = LyfteeScheduleSerializer(data=request_data)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LyfterServiceViewset(viewsets.ModelViewSet):
    queryset = LyfterService.objects.all()
    serializer_class = LyfterServiceSerializer

    def create(self, request, *args, **kwargs):
        print(request.data)
        user = request.user
        request_data = request.data.copy()
        request_data["user"] = user.id
        serializer = LyfterServiceSerializer(data=request_data)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
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
            PoolRide.objects.create(
                lyfter_service=lyfter_service_object,
                lyftee_schedule=candidate_lyftee_point.lyftee_schedule_obj,
                pickup_point_lat=candidate_lyftee_point.nearest_point[0],
                pickup_point_long=candidate_lyftee_point.nearest_point[1],
                timestamp=datetime.datetime.now()
            )
            serializer = LyfteeScheduleSerializer(candidate_lyftee_point.lyftee_schedule_obj)
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        return Response(data=[], status=status.HTTP_200_OK)