from django.db import models
from kratos.apps.app.models import App

class Pipeline(models.Model):
    app = models.ForeignKey(App, on_delete=models.CASCADE, related_name='task')
    name = models.CharField(max_length=100)
    stage = models.IntegerField(default=1)
    inuse = models.IntegerField(default=0)
    description = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 't_pipeline'
