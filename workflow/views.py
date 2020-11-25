from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from django.core.exceptions import ImproperlyConfigured

from workflow import serializers

class WorkflowViewSet(viewsets.GenericViewSet):
    '''
    CICD工作流
    '''
    serializer_classes = {
        'run': serializers.RunnerSerializer,
        'citrigger': serializers.CiTriggerSerializer,
        'status': serializers.RunnerStatusSerialier,
        'revoke': serializers.RunnerStatusSerialier
    }

    @action(methods=['POST', ], detail=False)
    def run(self, request):
        '''
        执行工作流
        '''
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    @action(methods=['POST', ], detail=False)
    def citrigger(self, request):
        '''
        部门CI流程触发
        '''
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(methods=['POST', ], detail=False)
    def status(self, request):
        '''
        工作流执行状态
        '''
        stat = self.get_serializer(data=request.data)
        stat.is_valid(raise_exception=True)
        return Response(stat.data)

    @action(methods=['POST', ], detail=False)
    def revoke(self, request):
        '''
        工作流执行状态
        '''
        stat = self.get_serializer(data=request.data)
        stat.is_valid(raise_exception=True)
        return Response(stat.data)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['action'] = self.action
        return context

    def get_serializer_class(self):
        if not isinstance(self.serializer_classes, dict):
            raise ImproperlyConfigured("serializer_classes should be a dict mapping.")

        if self.action in self.serializer_classes.keys():
            return self.serializer_classes[self.action]
        return super().get_serializer_class()
