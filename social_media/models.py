from django.contrib.auth import get_user_model
from django.db import models


class Post(models.Model):
    content = models.TextField()


class Follows(models.Model):
    followers = models.ForeignKey(
        get_user_model(), on_delete=models.DO_NOTHING, related_name="followers"
    )
    following = models.ForeignKey(
        get_user_model(), on_delete=models.DO_NOTHING, related_name="following"
    )
