from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="follower")
    follow = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="following")
    constraints = [
        models.UniqueConstraint(
            fields=['user', 'follow'],
            name='unique_follow',
        ),
    ]
