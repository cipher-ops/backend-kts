from rest_framework import serializers

from kratos.apps.pipeline.models import Pipeline
from kratos.apps.trigger.models import TriggerRecord

from kratos.apps.log.serializers import LogSerializer
from kratos.apps.pipeline.serializers import PipelineSerializer

from django.shortcuts import get_object_or_404

from celery.app.control import Control
from kratos.celery import app

from .async_executor import async_run

class RunnerSerializer(serializers.Serializer):
    pipeline = serializers.PrimaryKeyRelatedField(queryset=Pipeline.objects.all(), required=True, write_only=True)
    envs = serializers.JSONField(required=False, write_only=True, default={})
    logno = serializers.IntegerField(read_only=True)
    taskno = serializers.CharField(read_only=True)

    def create(self, obj):
        '''
        执行pipeline并更新日志
        '''
        pipeline = PipelineSerializer(obj['pipeline']).data

        logger = LogSerializer(data={'pipeline': pipeline['id'], 'status': 0})
        logger.is_valid(raise_exception=True)
        logger = logger.save()

        task = async_run.delay(pipeline, logger.id, obj['envs'])

        logger.taskno = task.id
        logger.envs = obj['envs']
        logger.save()

        return {'logno': logger.id, 'taskno': task.id}

class CiTriggerSerializer(serializers.ModelSerializer):
    logno = serializers.IntegerField(read_only=True)

    def create(self, obj):
        '''
        保存调用记录 触发pipeline执行
        '''
        trigger = TriggerRecord.objects.create(**obj)

        cipipeline = get_object_or_404(
            Pipeline, app__name = trigger.project,
            stage = 1,
            inuse = 1
        )
        
        runner = RunnerSerializer(data={'pipeline': cipipeline.id, 'envs': obj})
        runner.is_valid(raise_exception=True)
        runner.save()

        trigger.logno = runner.data['logno']
        trigger.taskno = runner.data['taskno']
        trigger.save()

        return trigger
    
    class Meta:
        model = TriggerRecord
        fields = ('id', 'project', 'oper', 'version', 'branch', 'issuekey', 'logno', 'taskno', 'created_at', 'updated_at')
        extra_kwargs = {'taskno': {'read_only': True}}

class RunnerStatusSerialier(serializers.Serializer):
    taskno = serializers.CharField(required=True)
    status = serializers.CharField(read_only=True)

    def to_representation(self, obj):
        '''
        对celery任务执行操作 返回celery任务状态
        '''
        action = self.context.get('action')
        if action == 'revoke':
            task_control = Control(app=app)
            task_control.revoke(str(obj['taskno']), terminate=True)
        task = async_run.AsyncResult(obj['taskno'])
        return {
            'taskno': obj['taskno'],
            'status': task.status
        }
