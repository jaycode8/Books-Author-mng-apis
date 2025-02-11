from django.db import models
from uuid import uuid4

# Create your models here.

class Author(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True, editable=False)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    email = models.CharField(max_length=100, unique=True)
    gender = models.CharField(max_length=10)
    password = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "author"
        verbose_name = "author"
        verbose_name_plural = "authors"

    def __str__(self):
        return self.title
