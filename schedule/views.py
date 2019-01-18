from rest_framework import viewsets

from schedule.factory import LyfteeScheduleFactory
from .models import LyfteeSchedule
from .models import LyfterService
from .serializers import LyfteeScheduleSerializer
from .serializers import LyfterServiceSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action


class LyfteeScheduleViewset(viewsets.ModelViewSet):
    queryset = LyfteeSchedule.objects.all()
    serializer_class = LyfteeScheduleSerializer

    def create(self, request, *args, **kwargs):
        user =request.user
        request_data = request.POST.copy()
        request_data["user"] = user.id
        serializer = LyfteeScheduleSerializer(data=request_data)

        if serializer.is_valid():
            print(serializer.validated_data)
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
        print("The data", request_data)
        serializer = LyfterServiceSerializer(data=request_data)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=True,
        url_path = "assign-lyftee",
        url_name = "assign-lyftee",
        methods=['post', ]
    )
    def assign_lyftee(self, request, *args, **kwargs):
        obj = self.get_object()

        # Remove this
        lyftee_schedule_object = LyfteeScheduleFactory()
        serializer = LyfteeScheduleSerializer(lyftee_schedule_object)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
