from rest_framework import viewsets
from kratos.apps.log import models, serializers
from rest_framework.response import Response
from rest_framework import status


class LogViewSet(viewsets.GenericViewSet):
    '''
    日志
    '''
    serializer_class = serializers.LogInfoSerializer
    queryset = models.Log.objects.all()

    def list(self, request):
        '''
        日志文件列表
        '''
        #serializer = serializers.LogSerializer(self.get_queryset(), many=True)
        #return Response(serializer.data)
        records = self.paginator.paginate_queryset(self.get_queryset(), self.request, view=self)
        serializer = self.get_serializer(records, many=True)
        return self.paginator.get_paginated_response(serializer.data)

    def retrieve(self, request, pk=None):
        '''
        读取日志文件
        '''
        serializer = self.get_serializer(self.get_object())
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        '''
        删除一条日志文件记录
        '''
        self.get_object().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
