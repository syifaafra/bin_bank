from datetime import datetime
from xmlrpc.client import MAXINT, MININT
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(default=datetime.now())
    amountKg = models.IntegerField()
    branchName = models.CharField(max_length=255)
    isFinished = models.BooleanField(default=False)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    points = models.IntegerField()



