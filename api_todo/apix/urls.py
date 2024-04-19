from rest_framework.routers import DefaultRouter
from apix.views import SensorViewSet

router = DefaultRouter()
router.register(r'', SensorViewSet)
urlpatterns = router.urls