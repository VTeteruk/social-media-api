from django.contrib.auth import get_user_model
from django.db import models


class Post(models.Model):
    creator = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True,
                                blank=True)
    name = models.CharField("Product Name", max_length=100, default="",
                            help_text="This is the help text")
    content = models.TextField(verbose_name='Concept', max_length=600,
                               blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
