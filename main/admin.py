from django.contrib import admin
from django.utils.html import format_html
from .models import ImageModel
from django.urls import reverse


@admin.register(ImageModel)
class ImageModelAdmin(admin.ModelAdmin):
    list_display = ("converted_image_tag", "download_webp_link", "download_png_link")
    readonly_fields = ["converted_image_tag", "converted_image"]

    def converted_image_tag(self, obj):
        if obj.converted_image:
            return format_html(
                '<img src="{}" width="150" height="auto" />', obj.converted_image.url
            )
        return "No image available"

    converted_image_tag.short_description = "Converted Image"

    def download_webp_link(self, obj):
        if obj.converted_image:
            return format_html(
                '<a href="{}" download>Download WebP</a>', obj.converted_image.url
            )
        return "No converted image available"

    download_webp_link.short_description = "Download WebP"

    def download_png_link(self, obj):
        if obj.converted_image:
            # 'convert_and_download_png'는 PNG 변환 및 다운로드 뷰의 URL 이름입니다.
            download_url = reverse("convert_and_download_png", kwargs={"pk": obj.pk})
            return format_html('<a href="{}">Download PNG</a>', download_url)
        return "No converted image available"

    download_png_link.short_description = "Download PNG"
