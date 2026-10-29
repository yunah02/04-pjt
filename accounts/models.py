from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    introduction = models.TextField(blank=True)
    followings = models.ManyToManyField('self', symmetrical=False, related_name = 'followers', blank = True)

