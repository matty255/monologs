from django.views.generic import View, TemplateView
from django.http import FileResponse, HttpResponseNotFound
from .models import ImageModel
from .utils import ImageConverter
from django.shortcuts import get_object_or_404
from pathlib import Path
from django.conf import settings
from PIL import Image
import io


class ConvertAndDownloadView(View):
    def get(self, request, *args, **kwargs):
        image_id = kwargs.get("pk")
        image_instance = get_object_or_404(ImageModel, pk=image_id)

        if image_instance.converted_image:
            file_path = settings.MEDIA_ROOT / image_instance.converted_image.name
            if file_path.exists():

                image = Image.open(file_path).convert("RGB")
                buffer = io.BytesIO()
                image.save(buffer, format="PNG")
                buffer.seek(0)

                return FileResponse(
                    buffer, as_attachment=True, filename=f"{file_path.stem}.png"
                )
        return HttpResponseNotFound("The requested file does not exist.")


class ConvertAndDownloadPNGView(View):
    def get(self, request, *args, **kwargs):
        image_id = kwargs.get("pk")
        image_instance = get_object_or_404(ImageModel, pk=image_id)

        if image_instance.converted_image:
            file_path = settings.MEDIA_ROOT / image_instance.converted_image.name
            if file_path.exists():
                image = Image.open(file_path).convert("RGB")
                buffer = io.BytesIO()
                image.save(buffer, format="PNG")
                buffer.seek(0)

                return FileResponse(
                    buffer, as_attachment=True, filename=f"{file_path.stem}.png"
                )
        return HttpResponseNotFound("The requested file does not exist.")


class IndexView(TemplateView):
    template_name = "main/index.html"


class AboutView(TemplateView):
    template_name = "main/about.html"
