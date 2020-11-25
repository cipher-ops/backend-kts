from django.db import models
from django_mysql.models import JSONField

class Tasktpl(models.Model):
    name = models.CharField(max_length=50)
    params = JSONField(blank=True, null=True)
    description = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 't_task_tpl'
