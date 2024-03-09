from django.contrib import admin
from .models import CustomUser, CroppedImage, Follow
from django.utils.html import format_html


# CustomUser 모델을 어드민 페이지에 등록하고, 위에서 정의한 액션을 추가
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = [
        "username",
        "profile_status",
        "profile_message",
    ]  # 어드민 목록에 표시될 필드


# CroppedImage 모델을 어드민 페이지에 등록
@admin.register(CroppedImage)
class CroppedImageAdmin(admin.ModelAdmin):
    list_display = ["id", "file_link", "uploaded"]  # 실제 모델에 존재하는 필드 사용

    def file_link(self, obj):
        return format_html("<a href='{url}'>View Image</a>", url=obj.file.url)

    file_link.short_description = "Image File"


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    search_fields = ["name"]
