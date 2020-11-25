from django.db import models
from django_mysql.models import JSONField
from kratos.apps.pipeline.models import Pipeline

class Log(models.Model):
    pipeline = models.ForeignKey(Pipeline, on_delete=models.CASCADE, related_name='log')
    envs = JSONField(blank=True, null=True)
    status = models.IntegerField(default=0)
    taskno = models.CharField(max_length=100, default="")
    duration = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 't_pipeline_log'
