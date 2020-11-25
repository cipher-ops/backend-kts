from django.db import models

class ServerKey(models.Model):
    name = models.CharField(max_length=100)
    ssh_port = models.IntegerField()
    ssh_user = models.CharField(max_length=100)
    ssh_pass = models.CharField(max_length=200)
    sudo_pass = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 't_server_key'

class Server(models.Model):
    inventory = models.ForeignKey(ServerKey, null=True, on_delete=models.SET_NULL, related_name='server')
    ipaddr = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 't_server'
