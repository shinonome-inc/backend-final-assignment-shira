from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    followees = models.ManyToManyField(
        "CustomUser",
        verbose_name="フォロー中のユーザー",
        through="FollowConnection",
        related_name="+",
        through_fields=("follower", "followee"),
    )
    followers = models.ManyToManyField(
        "CustomUser",
        verbose_name="フォローされているユーザー",
        through="FollowConnection",
        related_name="+",
        through_fields=("followee", "follower"),
    )


class FollowConnection(models.Model):
    follower = models.ForeignKey(
        "CustomUser",
        on_delete=models.CASCADE,
        related_name="followee_followconnections",
    )
    followee = models.ForeignKey(
        "CustomUser",
        on_delete=models.CASCADE,
        related_name="follower_followconnections",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["follower", "followee"], name="followconnection_unique"
            ),
        ]
