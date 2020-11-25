from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    phone = models.CharField(max_length=12, blank=True)
    wx_openid = models.CharField(max_length=40, blank=True)
