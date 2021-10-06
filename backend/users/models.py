from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="follower")
    follow = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="following")
