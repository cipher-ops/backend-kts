from rest_framework import routers
from kratos.apps.task.views import TaskViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register('task', TaskViewSet, basename='task')

urlpatterns = router.urls