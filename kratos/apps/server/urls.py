from rest_framework import routers
from kratos.apps.server.views import ServerViewSet, ServerKeyViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register('server', ServerViewSet, basename='server')
router.register('credential', ServerKeyViewSet, basename='server-key')

urlpatterns = router.urls
