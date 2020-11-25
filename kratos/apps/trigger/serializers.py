from rest_framework import serializers
from kratos.apps.trigger import models

class TriggerRecordSerializer(serializers.ModelSerializer):

  class Meta:
    model = models.TriggerRecord
    fields = ('id', 'project', 'oper', 'version', 'branch', 'issuekey', 'created_at', 'updated_at')
