import os
from rest_framework import serializers
from kratos.apps.log.models import Log
from django.conf import settings


class LogInfoSerializer(serializers.ModelSerializer):
    path = serializers.SerializerMethodField()
    content = serializers.SerializerMethodField()

    def get_path(self, instance):
        return os.path.join(settings.BASE_DIR, 'logs/pipeline', str(instance.id) + '.log')

    def get_content(self, instance):
        filename = self.get_path(instance)
        content = ""
        if not os.path.isfile(filename):
            print('File does not exist.')
        else:
            with open(filename) as f:
                content = f.read().splitlines()
        return content

    class Meta:
        model = Log
        fields = ('id', 'pipeline', 'envs', 'status', 'taskno', 'duration', 'path', 'content', 'created_at', 'updated_at')


class LogSerializer(serializers.ModelSerializer):
    path = serializers.SerializerMethodField()

    def get_path(self, instance):
        return os.path.join(settings.BASE_DIR, 'logs/pipeline', str(instance.id) + '.log')

    class Meta:
        model = Log
        fields = ('id', 'pipeline', 'envs', 'status', 'taskno', 'duration', 'path',  'created_at', 'updated_at')