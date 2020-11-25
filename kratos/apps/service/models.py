from django.db import models
from kratos.apps.server.models import Server
from kratos.apps.app.models import App

class Service(models.Model):
    server = models.ForeignKey(Server, on_delete=models.CASCADE, related_name='service')
    app = models.ForeignKey(App, on_delete=models.CASCADE, related_name='service')
    app_version = models.CharField(max_length=50, blank=True, null=True)
    config_version = models.CharField(max_length=50, blank=True, null=True)
    status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 't_service'
