from django.contrib import admin
from kratos.apps.server.models import Server, ServerKey

admin.site.register(Server)
admin.site.register(ServerKey)
