from django.db import models
from django_mysql.models import JSONField
from kratos.apps.pipeline.models import Pipeline
from kratos.apps.tasktpl.models import Tasktpl


class Task(models.Model):
    pipeline = models.ForeignKey(Pipeline, on_delete=models.CASCADE, related_name='task')
    tasktpl = models.ForeignKey(Tasktpl, on_delete=models.CASCADE, related_name='task')
    params = JSONField()
    stage = models.IntegerField(default=1)
    seq = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 't_task'
