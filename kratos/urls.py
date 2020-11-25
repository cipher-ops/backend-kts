"""kratos URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('openapi', get_schema_view(
        title='kts',
        description='API文档',
        version='1.2.0.1'
    ), name='openapi-schema'),

    path('swagger-ui/', TemplateView.as_view(
        template_name='swagger-ui.html',
        extra_context={'schema_url': 'openapi-schema'}
    ), name='swagger-ui'),

    path('redoc/', TemplateView.as_view(
        template_name='redoc.html',
        extra_context={'schema_url': 'openapi-schema'}
    ), name='redoc'),

    url(r'^api/v1/', include(([
        path('', include('kratos.apps.auth.urls')),
        path('', include('kratos.apps.app.urls')),
        path('', include('kratos.apps.tasktpl.urls')),
        path('', include('kratos.apps.task.urls')),
        path('', include('kratos.apps.artifact.urls')),
        path('', include('kratos.apps.server.urls')),
        path('', include('kratos.apps.pipeline.urls')),
        path('', include('kratos.apps.configuration.urls')),
        path('', include('kratos.apps.log.urls')),
        path('', include('kratos.apps.service.urls')),
        path('', include('kratos.apps.trigger.urls')),
        path('', include('workflow.urls'))
    ], 'api-v1'), namespace='v1'))

]

urlpatterns += staticfiles_urlpatterns()
