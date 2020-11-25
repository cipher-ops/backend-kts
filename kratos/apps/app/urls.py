from rest_framework import routers
from kratos.apps.app.views import AppViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register('app', AppViewSet, basename='app')

urlpatterns = router.urls
