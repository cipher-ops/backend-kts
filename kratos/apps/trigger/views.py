from rest_framework import viewsets
from kratos.apps.trigger import models, serializers

class TriggerViewSet(viewsets.GenericViewSet):
  '''
  Trigger信息
  '''
  serializer_class = serializers.TriggerRecordSerializer
  queryset = models.TriggerRecord.objects.all()

  def list(self, request):
    '''
    Trigger调用记录列表
    '''
    records = self.paginator.paginate_queryset(self.get_queryset(), self.request, view=self)
    serializer = self.get_serializer(records, many=True)
    return self.paginator.get_paginated_response(serializer.data)
