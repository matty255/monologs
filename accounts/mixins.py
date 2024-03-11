import uuid
from datetime import datetime
from django.contrib.contenttypes.models import ContentType
from django.apps import apps


class UploadToPathMixin:
    @staticmethod
    def upload_to_original(instance, filename):
        ext = filename.split(".")[-1]
        filename = f"{uuid.uuid4()}.{ext}"  # 고유한 파일 이름 생성
        return f"original_images/{datetime.now().strftime('%Y/%m/%d')}/{filename}"

    @staticmethod
    def upload_to_cropped(instance, filename):
        ext = filename.split(".")[-1]
        filename = f"{uuid.uuid4()}.{ext}"  # 고유한 파일 이름 생성
        return f"cropped_images/{datetime.now().strftime('%Y/%m/%d')}/{filename}"

    @staticmethod
    def upload_to_user_path(instance, filename, folder_name):
        username = instance.user.username  # Assuming the user is linked to the instance
        ext = filename.split(".")[-1]
        filename = f"{uuid.uuid4()}.{ext}"  # 고유한 파일 이름 생성
        date_path = datetime.now().strftime("%Y/%m/%d")
        return f"{folder_name}/{username}/{date_path}/{filename}"


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
