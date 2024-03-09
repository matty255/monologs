# mixins.py

from datetime import datetime


class UploadToPathMixin:
    def upload_to(self, instance, filename):
        return "thumbnails/{0}/{1}".format(
            datetime.now().strftime("%Y/%m/%d"), filename
        )
