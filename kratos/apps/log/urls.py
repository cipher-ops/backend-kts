from rest_framework import routers
from kratos.apps.log.views import LogViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register('log', LogViewSet, basename='log')

urlpatterns = router.urls
