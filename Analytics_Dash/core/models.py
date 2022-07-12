from django.db import models
from django.contrib.auth.models import User


class UserRole(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=[('manager', 'manager'), ('member', 'member')], default='member')


class AppInstalls(models.Model):
    idate=models.DateField()
    package_name=models.CharField(max_length=500)
    carrier=models.CharField(max_length=200)
    daily_device_installs = models.IntegerField()
    active_device_installs = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True,null=True)


class Apps(models.Model):
    name=models.CharField(max_length=500)
    app_name=models.CharField(max_length=500)
    app_id=models.CharField(max_length=500)
    image_link=models.URLField()