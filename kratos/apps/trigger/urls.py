from rest_framework import routers
from kratos.apps.trigger.views import TriggerViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register('trigger-record', TriggerViewSet, basename='trigger')

urlpatterns = router.urls