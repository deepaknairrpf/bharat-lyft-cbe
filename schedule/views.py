from rest_framework import viewsets
from .models import LyfteeSchedule
from .serializers import LyfteeScheduleSerializer
from rest_framework.response import Response
from rest_framework import status

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
