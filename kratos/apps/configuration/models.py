from django.db import models
from kratos.apps.app.models import App


class Configuration(models.Model):
    version = models.CharField(max_length=50, blank=True, null=True)
    name = models.CharField(max_length=100)
    path = models.CharField(max_length=200, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    app = models.ForeignKey(App, on_delete=models.CASCADE, related_name='configuration')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 't_configuration'
