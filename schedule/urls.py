from rest_framework.routers import SimpleRouter
from .views import LyfteeSchedule

router = SimpleRouter()

router.register('lyftee-schedules', LyfteeSchedule, base_name="lyftee-schedule")