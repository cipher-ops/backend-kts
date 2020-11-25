from rest_framework import serializers
from kratos.apps.server import models

class ServerKeySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ServerKey
        fields = ('id', 'name', 'ssh_port', 'ssh_user', 'ssh_pass', 'sudo_pass')

class ServerSerializer(serializers.ModelSerializer):
    credential = ServerKeySerializer(read_only=True, source='inventory')

    class Meta:
        model = models.Server
        fields = ('id', 'ipaddr', 'inventory', 'credential')
        extra_kwargs = {'inventory': {'write_only': True, 'required': False}}
