from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    profile_picture = models.ImageField(
        upload_to="profile_pictures/", null=True, blank=True
    )
    profile_status = models.CharField(max_length=200, null=True, blank=True)
    profile_message = models.TextField(null=True, blank=True)
