from PIL import Image
from pathlib import Path


class ImageConverter:
    @staticmethod
    def convert_to_webp(source_path):
        destination_path = Path(source_path).with_suffix(".webp")
        with Image.open(source_path) as img:
            img.convert("RGB").save(destination_path, "webp")
        return destination_path
