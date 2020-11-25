from rest_framework import viewsets
from kratos.apps.server import models, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

class ServerViewSet(viewsets.GenericViewSet):
    '''
    服务器信息
    '''
    serializer_class = serializers.ServerSerializer
    queryset = models.Server.objects.all()
    serializer_classes = {
        'key': serializers.ServerKeySerializer
    }
    querysets = {
        'key': models.ServerKey.objects.all()
    }

    def list(self, request):
        '''
        服务器列表
        '''
        records = self.paginator.paginate_queryset(self.get_queryset(), self.request, view=self)
        serializer = self.get_serializer(records, many=True)
        return self.paginator.get_paginated_response(serializer.data)

    def retrieve(self, request, pk=None):
        '''
        服务器详情
        '''
        serializer = self.get_serializer(self.get_object())
        return Response(serializer.data)

    def create(self, request):
        '''
        新增服务器
        '''
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        '''
        服务器信息更新
        '''
        serializer = self.get_serializer(self.get_object(), data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        '''
        删除一条服务器记录
        '''
        self.get_object().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_serializer_class(self):
        if self.action in self.serializer_classes.keys():
            return self.serializer_classes[self.action]
        return super().get_serializer_class()

    def get_queryset(self):
        if self.action in self.querysets.keys():
            return self.querysets[self.action]
        return super().get_queryset()

class ServerKeyViewSet(viewsets.GenericViewSet):
    '''
    服务器凭证信息
    '''
    serializer_class = serializers.ServerKeySerializer
    queryset = models.ServerKey.objects.all()

    def list(self, request):
        '''
        服务器凭证信息列表
        '''
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        '''
        服务器凭证详情
        '''
        serializer = self.get_serializer(self.get_object())
        return Response(serializer.data)

    def create(self, request):
        '''
        新增一条服务器凭证
        '''
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def partial_update(self, request, pk=None):
        '''
        服务器凭证信息更新
        '''
        serializer = self.get_serializer(self.get_object(), data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        '''
        删除一条服务器凭证记录
        '''
        self.get_object().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
