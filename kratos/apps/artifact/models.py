from django.db import models
from kratos.apps.app.models import App


class Artifact(models.Model):
    app = models.ForeignKey(App, on_delete=models.CASCADE, related_name='artifact')
    artifact_type = models.IntegerField()
    version = models.CharField(max_length=50, blank=True, null=True)
    download_url = models.CharField(u'下载地址', max_length=200, blank=True, null=True)
    size = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 't_artifact'
