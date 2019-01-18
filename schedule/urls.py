from rest_framework.routers import SimpleRouter
from .views import LyfteeScheduleViewset
from .views import LyfterServiceViewset

router = SimpleRouter()

router.register('lyftee-schedules', LyfteeScheduleViewset, base_name="lyftee-schedule")
router.register('lyfter-services', LyfterServiceViewset, base_name="lyfter-service")
urlpatterns = router.urls