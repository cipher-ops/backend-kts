from rest_framework import viewsets
from kratos.apps.service import models, serializers
from rest_framework.response import Response
from rest_framework import status


class ServiceViewSet(viewsets.GenericViewSet):
    '''
    服务
    '''
    serializer_class = serializers.ServiceSerializer
    queryset = models.Service.objects.all()

    def list(self, request):
        '''
        服务列表
        '''
        records = self.paginator.paginate_queryset(self.get_queryset(), self.request, view=self)
        serializer = self.get_serializer(records, many=True)
        return self.paginator.get_paginated_response(serializer.data)

    def retrieve(self, request, pk=None):
        '''
        服务详情
        '''
        serializer = self.get_serializer(self.get_object())
        return Response(serializer.data)

    def create(self, request):
        '''
        新增服务
        '''
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        '''
        服务信息更新
        '''
        serializer = self.get_serializer(self.get_object(), data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        '''
        删除一条服务记录
        '''
        self.get_object().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
