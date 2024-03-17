import uuid
from datetime import datetime
from django.contrib.contenttypes.models import ContentType
from django.apps import apps


class UploadToPathMixin:
    base_folder = "uploads"
    user_folder = "user_folder"  # 클래스 변수로 설정

    @staticmethod
    def upload_to(instance, filename):
        folder_name = str(uuid.uuid4())
        return f"{UploadToPathMixin.base_folder}/{folder_name}/{datetime.now().strftime('%Y/%m/%d')}/{filename}"

    @staticmethod
    def upload_to_user_path(instance, filename):
        folder_name = str(uuid.uuid4())
        user_path = f"{UploadToPathMixin.user_folder}/{instance.user.username}"  # 클래스 변수 사용
        return f"{UploadToPathMixin.base_folder}/{user_path}/{folder_name}/{datetime.now().strftime('%Y/%m/%d')}/{filename}"


class LikedAndBookmarkedMixin:
    def get_liked_and_bookmarked_objects(self, user, model_classes):
        context = {}
        for model_class in model_classes:
            model_name = (
                model_class.__name__.lower()
            )  # 모델 이름을 소문자로 변환 (예: 'Post' -> 'liked_posts')
            content_type = ContentType.objects.get_for_model(model_class)

            # ContentType을 기반으로 좋아요한 객체 목록 조회
            Like = apps.get_model("blog", "Like")
            liked_objects_ids = Like.objects.filter(
                user=user, content_type=content_type
            ).values_list("object_id", flat=True)
            context[f"liked_{model_name}s"] = model_class.objects.filter(
                pk__in=liked_objects_ids
            )

            # ContentType을 기반으로 북마크한 객체 목록 조회
            Bookmark = apps.get_model("blog", "Bookmark")
            bookmarked_objects_ids = Bookmark.objects.filter(
                user=user, content_type=content_type
            ).values_list("object_id", flat=True)
            context[f"bookmarked_{model_name}s"] = model_class.objects.filter(
                pk__in=bookmarked_objects_ids
            )

        return context
