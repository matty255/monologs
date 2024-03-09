from django.contrib import admin
from django.utils.html import format_html
from .models import ImageModel


@admin.register(ImageModel)
class ImageModelAdmin(admin.ModelAdmin):
    list_display = ("image_tag", "download_link")
    readonly_fields = ["image_tag", "converted_image"]

    def image_tag(self, obj):
        return format_html('<img src="{}" width="150" height="auto" />', obj.image.url)

    image_tag.short_description = "Image"

    def download_link(self, obj):
        if obj.converted_image:
            return format_html(
                '<a href="{}" download>Download WebP</a>', obj.converted_image.url
            )
        return "Conversion needed"

    download_link.short_description = "Download WebP"
