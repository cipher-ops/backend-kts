from rest_framework import serializers
from kratos.apps.pipeline.models import Pipeline
from kratos.apps.task.serializers import TaskSerializer as TaskField
from kratos.apps.app.serializers import AppSerializer as AppField

class PipelineListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Pipeline
        fields = ('id', 'name', 'description', 'created_at', 'updated_at')

class PipelineSerializer(serializers.ModelSerializer):
    appinfo = AppField(read_only=True, source='app')
    tasks = serializers.SerializerMethodField()

    def get_tasks(self, instance):
        tasks = instance.task.all().order_by('stage', 'seq')
        return TaskField(tasks, many=True).data

    class Meta:
        model = Pipeline
        fields = ('id', 'name', 'app', 'tasks', 'description', 'appinfo')
        extra_kwargs = {'app': {'write_only': True, 'required': False}}
        