from rest_framework import serializers
from kratos.apps.artifact.models import Artifact
from kratos.apps.app.serializers import AppSerializer


class ArtifactSerializer(serializers.ModelSerializer):
    appinfo = AppSerializer(read_only=True, source='app')

    class Meta:
        model = Artifact
        fields = ('id', 'artifact_type', 'version', 'download_url', 'size', 'created_at', 'updated_at', 'app', 'appinfo')
        extra_kwargs = {'app': {'write_only': True, 'required': False}}
