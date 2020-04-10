from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.dispatch import receiver
from django.db.models.signals import post_save


class User(AbstractUser):
    pass


class Profile(models.Model):
    bio = models.TextField(blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
