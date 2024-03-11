# mixins.py
import uuid
from datetime import datetime
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.models import ContentType
from django.apps import apps


class UploadToPathMixin:
    staticmethod

    def upload_to(self, instance, filename):
        ext = filename.split(".")[-1]
        filename = f"{uuid.uuid4()}.{ext}"
        return f"thumbnails/{datetime.now().strftime('%Y/%m/%d')}/{filename}"


class LikeMixin:
    def get_like_status(self, user, instance):
        if not user.is_authenticated:
            return False
        Like = apps.get_model(
            "blog", "Like"
        )  # 'app_name'을 Like 모델이 정의된 앱의 이름으로 변경해야 합니다.
        content_type = ContentType.objects.get_for_model(instance.__class__)
        liked = Like.objects.filter(
            content_type=content_type, object_id=instance.id, user=user
        ).exists()
        return liked


class BookmarkMixin:
    def get_bookmark_status(self, user, instance):
        if not user.is_authenticated:
            return False
        Bookmark = apps.get_model(
            "blog", "Bookmark"
        )  # 'app_name'을 Bookmark 모델이 정의된 앱의 이름으로 변경해야 합니다.
        content_type = ContentType.objects.get_for_model(instance.__class__)
        bookmarked = Bookmark.objects.filter(
            content_type=content_type, object_id=instance.id, user=user
        ).exists()
        return bookmarked
