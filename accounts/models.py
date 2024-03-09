from django.db import models
from django.contrib.auth.models import AbstractUser
from .mixins import UploadToPathMixin
from django.conf import settings


class CustomUser(AbstractUser):
    profile_status = models.CharField(max_length=200, null=True, blank=True)
    profile_message = models.TextField(null=True, blank=True)
    profile_picture = models.OneToOneField(
        "CroppedImage",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="user",
    )


class Follow(models.Model):
    follower = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="following", on_delete=models.CASCADE
    )
    following = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="followers", on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ("follower", "following")


class CroppedImage(UploadToPathMixin, models.Model):
    original_file = models.ImageField(upload_to=UploadToPathMixin.upload_to_original)
    file = models.ImageField(upload_to=UploadToPathMixin.upload_to_cropped)
    uploaded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.pk)

    @property
    def url(self):
        return self.file.url
