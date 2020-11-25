from django.db import models

class TriggerRecord(models.Model):
  project = models.CharField(max_length=100)
  oper = models.CharField(max_length=100)
  version = models.CharField(max_length=100)
  branch = models.CharField(max_length=100)
  issuekey = models.CharField(max_length=100)
  taskno = models.CharField(max_length=100, null=True, default="")
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    db_table = 't_trigger_record'
