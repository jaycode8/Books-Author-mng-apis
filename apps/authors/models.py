from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from uuid import uuid4
from datetime import datetime

# Create your models here.

class AuthorManager(BaseUserManager):
    def create_author(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError("username is required")
        if not email:
            raise ValueError("email field is required")
        email = self.normalize_email(email)
        author = self.model(username=username, password=password, **extra_fields)
        author.set_password(password)
        author.save()
        return author

class Author(AbstractBaseUser):
    id = models.UUIDField(default=uuid4, primary_key=True, editable=False)
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True)
    email = models.CharField(max_length=255, unique=True)
    gender = models.CharField(max_length=10)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email','id_no','phone']

    objects = AuthorManager()

    class Meta:
        db_table = "author"
        verbose_name = "author"
        verbose_name_plural = "authors"

    
    def __str__(self):
        return self.email

    def has_module_perms(self, app_label):
        return True

    def has_perm(self, perm, obj=None):
        return True



