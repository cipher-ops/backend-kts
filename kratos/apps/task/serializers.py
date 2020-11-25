from rest_framework import serializers
from kratos.apps.task.models import Task


class TaskSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    def get_name(self, instance):
        return instance.tasktpl.name

    class Meta:
        model = Task
        fields = ('id', 'name', 'params', 'stage', 'seq', 'pipeline', 'tasktpl')