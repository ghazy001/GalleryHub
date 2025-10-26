from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # already has: username, email, password, is_active, is_staff, etc.
    is_banned = models.BooleanField(default=False)
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    # example extra fields, optional:


    def __str__(self):
        return self.username
