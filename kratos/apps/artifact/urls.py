from rest_framework import routers
from kratos.apps.artifact.views import ArtifactViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register('artifact', ArtifactViewSet, basename='artifact')

urlpatterns = router.urls
