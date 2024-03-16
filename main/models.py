from django.db import models
from django.conf import settings
from pathlib import Path
from PIL import Image
from django.core.files.base import ContentFile
import io


class ImageModel(models.Model):
    image = models.ImageField(upload_to="images/", max_length=500)
    converted_image = models.FileField(
        upload_to="converted_images/", blank=True, null=True, max_length=500
    )

    def save(self, *args, **kwargs):
        # 임시 메모리에 이미지를 WebP로 변환
        if self.image:  # 이미지 필드가 채워져 있으면
            pil_image = Image.open(self.image)
            pil_image = pil_image.convert("RGB")  # PNG 등의 투명 이미지 처리를 위해
            buffer = io.BytesIO()
            pil_image.save(buffer, format="WEBP")
            buffer.seek(0)

            # 변환된 이미지 파일명 설정
            original_name = Path(self.image.name).stem  # 확장자 없는 파일 이름
            webp_filename = f"{original_name}.webp"

            # 변환된 이미지를 converted_image 필드에 저장
            self.converted_image.save(
                webp_filename, ContentFile(buffer.read()), save=False
            )
            buffer.close()

            # 원본 이미지 필드를 None으로 설정하여 저장하지 않음
            self.image = None

        super().save(*args, **kwargs)  # 변환된 이미지 정보 저장

    def __str__(self):
        return self.converted_image.name if self.converted_image else "No image"
