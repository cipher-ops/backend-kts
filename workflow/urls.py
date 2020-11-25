from rest_framework import routers
from workflow.views import WorkflowViewSet


router = routers.DefaultRouter(trailing_slash=False)
router.register('workflow', WorkflowViewSet, basename='workflow')

urlpatterns = router.urls
