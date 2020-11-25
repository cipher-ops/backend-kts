from rest_framework import routers
from kratos.apps.pipeline.views import PiplineViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register('pipeline', PiplineViewSet, basename='pipline')

urlpatterns = router.urls

