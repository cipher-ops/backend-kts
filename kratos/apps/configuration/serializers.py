from rest_framework import serializers
from kratos.apps.configuration.models import Configuration
from kratos.apps.app.serializers import AppSerializer


class ConfigurationSerializer(serializers.ModelSerializer):
    appinfo = AppSerializer(read_only=True, source='app')

    class Meta:
        model = Configuration
        fields = ('id', 'version', 'name', 'path', 'content', 'app', 'appinfo', 'created_at', 'updated_at')
        extra_kwargs = {'app': {'write_only': True, 'required': False}}
