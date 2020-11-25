from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from kratos.apps.pipeline import models, serializers
from rest_framework.response import Response
from rest_framework import status


class PiplineViewSet(viewsets.GenericViewSet):
    '''
    流水线
    '''
    serializer_class = serializers.PipelineSerializer
    queryset = models.Pipeline.objects.all()

    def list(self, request):
        '''
        流水线列表
        '''
        records = self.paginator.paginate_queryset(self.get_queryset(), self.request, view=self)
        serializer = self.get_serializer(records, many=True)
        return self.paginator.get_paginated_response(serializer.data)

    def retrieve(self, request, pk=None):
        '''
        流水线详情
        '''
        serializer = self.get_serializer(self.get_object())
        return Response(serializer.data)

    def create(self, request):
        '''
        新增流水线
        '''
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        '''
        流水线信息更新
        '''
        serializer = self.get_serializer(self.get_object(), data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        '''
        删除一条流水线记录
        '''
        self.get_object().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
