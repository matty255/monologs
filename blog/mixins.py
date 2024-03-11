# mixins.py
import uuid
from datetime import datetime
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.models import ContentType
from django.apps import apps
from django.forms import ModelChoiceField
from django.utils.html import format_html
from django.shortcuts import get_object_or_404


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


# class TreeViewMixin:

#     def get_descendants(self, user, category_id, include_self=True):

#         node = get_object_or_404(Category, pk=category_id, author=user)
#         descendants = node.descendants(include_self=include_self).filter(author=user)
#         return descendants


class IndentMixin:
    def get_level(self, obj):
        # obj의 tree_depth 속성을 사용하여 노드의 깊이를 반환합니다.
        return getattr(obj, "tree_depth", 0)

    def label_from_instance(self, obj):
        # get_level 메소드를 사용하여 들여쓰기를 적용합니다.
        prefix = "----" * self.get_level(obj)
        return format_html("{} {}", prefix, obj.name)


class CustomModelChoiceField(IndentMixin, ModelChoiceField):
    pass
