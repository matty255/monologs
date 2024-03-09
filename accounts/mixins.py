from datetime import datetime


class UploadToPathMixin:
    @staticmethod
    def upload_to_original(instance, filename):
        return "original_images/{0}/{1}".format(
            datetime.now().strftime("%Y/%m/%d"), filename
        )

    @staticmethod
    def upload_to_cropped(instance, filename):
        return "cropped_images/{0}/{1}".format(
            datetime.now().strftime("%Y/%m/%d"), filename
        )
