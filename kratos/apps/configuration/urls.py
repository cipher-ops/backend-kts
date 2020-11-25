from rest_framework import routers
from kratos.apps.configuration.views import ConfigurationViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register('configuration', ConfigurationViewSet, basename='configuration')

urlpatterns = router.urls
