from rest_framework import viewsets
from .models import LyfteeSchedule
from .serializers import LyfteeScheduleSerializer


class LyfteeScheduleViewset(viewsets.ModelViewSet):
    queryset = LyfteeSchedule.objects.all()
    serializer_class = LyfteeScheduleSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        print(request.data)
