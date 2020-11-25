from rest_framework import routers
from kratos.apps.service.views import ServiceViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register('service', ServiceViewSet, basename='service')

urlpatterns = router.urls

