import os
import uuid

from django.contrib.auth import get_user_model
from django.db import models


def get_unique_pass(instance, filename):
    _, ext = os.path.splitext(filename)

    filename = f"{instance.creator.email}-{uuid.uuid4()}{ext}"

    return os.path.join("uploads", "posts", filename)


class Post(models.Model):
    creator = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    name = models.CharField(
        "Product Name",
        max_length=100,
        default="New post",
    )
    content = models.TextField(
        verbose_name="Content", max_length=600, blank=True
    )
    image = models.ImageField(null=True, upload_to=get_unique_pass)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
