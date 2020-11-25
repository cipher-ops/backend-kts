from rest_framework import viewsets
from kratos.apps.task.serializers import TaskSerializer
from rest_framework.response import Response
from kratos.apps.task import models
from rest_framework import status


class TaskViewSet(viewsets.GenericViewSet):
    '''
    任务
    '''
    serializer_class = TaskSerializer
    queryset = models.Task.objects.all()

    def list(self, request):
        '''
        任务列表
        '''
        records = self.paginator.paginate_queryset(self.get_queryset(), self.request, view=self)
        serializer = self.get_serializer(records, many=True)
        return self.paginator.get_paginated_response(serializer.data)

    def retrieve(self, request, pk=None):
        '''
        任务详情
        '''
        serializer = self.get_serializer(self.get_object())
        return Response(serializer.data)

    def create(self, request):
        '''
        新增任务
        '''
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        '''
        任务信息更新
        '''
        serializer = self.get_serializer(self.get_object(), data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        '''
        删除一条任务记录
        '''
        self.get_object().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
