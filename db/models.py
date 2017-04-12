from __future__ import unicode_literals
from django.db import models

# python3 manage.py makemigrations
# python3 manage.py migrate

# Create your models here.
from django.utils import timezone

class webshell(models.Model):
    remarks = models.CharField(max_length=50)
    links = models.CharField(max_length=255)
    passwd = models.CharField(max_length=255)
    type = models.CharField(max_length=4)
    ponypath = models.CharField(max_length=255)
    desk = models.CharField(max_length=255)
    information = models.CharField(max_length=255)
    time = models.DateTimeField(default=timezone.now)
    temp = models.CharField(max_length=255,blank=True)