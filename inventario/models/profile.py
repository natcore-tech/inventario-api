# store/models/profile.py
import uuid
from pathlib import Path
from django.db import models
from django.contrib.auth.models import User


def avatar_upload_path(instance, filename):
    ext = Path(filename).suffix.lower()
    return f'avatars/user_{instance.user_id}/{uuid.uuid4()}{ext}'


class UserProfile(models.Model):
    user   = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to=avatar_upload_path, blank=True, null=True)

    def __str__(self):
        return f'Profile of {self.user.username}'