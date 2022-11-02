from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.db import models
from django.utils import timezone
from xmlrpc.client import MAXINT, MININT
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.db import models

from project_django import settings

User = settings.AUTH_USER_MODEL


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(default=timezone.now)
    amountKg = models.IntegerField()
    branchName = models.CharField(max_length=255)
    isFinished = models.BooleanField(default=False)


class MyUserManager(BaseUserManager):
    def create_user(self, username, password=None):
        user = self.model(
            username=username
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            password=password,
            username=username,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    username = models.CharField(max_length=20, unique=True)
    points = models.IntegerField(default=0)

    is_admin = models.BooleanField(default=False)
    objects = MyUserManager()

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Article(models.Model):
    title = models.CharField(max_length=100)
    intro = models.TextField()
    image = models.CharField(max_length=500)
    source = models.URLField()

class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, default=None)
    date = models.DateField(default=timezone.now)
    subject = models.CharField(max_length=255)
    feedback = models.TextField()
