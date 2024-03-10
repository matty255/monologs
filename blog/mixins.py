# mixins.py
import uuid
from datetime import datetime


class UploadToPathMixin:
    staticmethod

    def upload_to(self, instance, filename):
        ext = filename.split(".")[-1]
        filename = f"{uuid.uuid4()}.{ext}"
        return f"thumbnails/{datetime.now().strftime('%Y/%m/%d')}/{filename}"
