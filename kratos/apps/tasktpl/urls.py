from rest_framework import routers
from kratos.apps.tasktpl.views import TasktplViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register('tasktpl', TasktplViewSet, basename='tasktpl')

urlpatterns = router.urls
