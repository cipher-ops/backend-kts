from rest_framework import serializers
from kratos.apps.service import models

class ServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Service
        fields = ('id', 'server', 'app', 'app_version', 'config_version', 'created_at', 'updated_at')
        extra_kwargs = {'status': {'required': False}, 'config_version': {'required': False}}
