from django.db import models

class App(models.Model):
    name = models.CharField(max_length=100)
    app_type = models.CharField(max_length=50, blank=True, null=True)
    repo_url = models.CharField(u'仓库地址', max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 't_app'
