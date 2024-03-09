from django.views.generic import View, TemplateView
from django.http import FileResponse, HttpResponseNotFound
from .models import ImageModel
from .utils import ImageConverter
from django.shortcuts import get_object_or_404
from pathlib import Path
from django.conf import settings


class ConvertAndDownloadView(View):
    def get(self, request, *args, **kwargs):
        image_id = kwargs.get("pk")
        image_instance = get_object_or_404(ImageModel, pk=image_id)

        if not image_instance.converted_image:
            # 이미지 변환 처리
            source_path = image_instance.image.path
            converted_path = ImageConverter.convert_to_webp(source_path)
            image_instance.converted_image.name = str(
                Path(converted_path).relative_to(settings.MEDIA_ROOT)
            )
            image_instance.save()

        # 변환된 이미지 다운로드
        file_path = settings.MEDIA_ROOT / image_instance.converted_image.name
        if file_path.exists():
            return FileResponse(
                open(file_path, "rb"), as_attachment=True, filename=file_path.name
            )
        else:
            return HttpResponseNotFound("The requested webp file does not exist.")


class IndexView(TemplateView):
    template_name = "main/index.html"


class AboutView(TemplateView):
    template_name = "main/about.html"
