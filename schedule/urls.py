from rest_framework.routers import SimpleRouter
from .views import LyfteeScheduleViewset

router = SimpleRouter()

router.register('lyftee-schedules', LyfteeScheduleViewset, base_name="lyftee-schedule")
urlpatterns = router.urls