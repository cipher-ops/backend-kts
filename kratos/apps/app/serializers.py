from rest_framework import serializers
from kratos.apps.app.models import App


class AppSerializer(serializers.ModelSerializer):

    class Meta:
        model = App
        fields = ('id', 'name', 'app_type', 'repo_url', 'created_at', 'updated_at')
