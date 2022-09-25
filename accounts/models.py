from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    pass


class Follower(models.Model):
    follower = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    followee_list = models.ManyToManyField(
        CustomUser, related_name="followee_list", blank=True
    )

    def __str__(self):
        return self.follower
