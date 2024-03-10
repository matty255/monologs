import uuid
from datetime import datetime


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
