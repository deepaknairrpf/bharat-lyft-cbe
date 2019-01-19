from rest_framework.routers import SimpleRouter
from .views import LyfteeScheduleViewset
from .views import LyfterServiceViewset
from .views import PoolRideViewset

router = SimpleRouter(trailing_slash=False)

router.register('lyftee-schedules', LyfteeScheduleViewset, base_name="lyftee-schedule")
router.register('lyfter-services', LyfterServiceViewset, base_name="lyfter-service")
router.register('pool-ride', PoolRideViewset, basename="pool-ride")

urlpatterns = router.urls