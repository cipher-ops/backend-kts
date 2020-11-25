from rest_framework import serializers
from kratos.apps.tasktpl.models import Tasktpl

class TasktplSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tasktpl
        fields = ('id', 'name', 'params', 'description')
