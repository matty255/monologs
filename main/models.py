from django.db import models
from django.conf import settings
from pathlib import Path
from PIL import Image


class ImageModel(models.Model):
    image = models.ImageField(upload_to="images/", max_length=500)
    converted_image = models.FileField(
        upload_to="converted_images/", blank=True, null=True, max_length=500
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # 원본 이미지 저장
        if self.image:  # 이미지 필드가 채워져 있으면
            # 이미지를 WebP로 변환
            source_path = self.image.path
            destination_path = Path(source_path).with_suffix(".webp")
            with Image.open(source_path) as img:
                img.convert("RGB").save(destination_path, "webp")

            # 변환된 이미지 경로 저장
            self.converted_image.name = str(
                destination_path.relative_to(settings.MEDIA_ROOT)
            )
            super().save(*args, **kwargs)  # 변환된 이미지 정보 저장

    def __str__(self):
        return self.image.name
