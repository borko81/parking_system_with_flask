import cloudinary
import cloudinary.uploader
from decouple import config


class Cloudinary:

    def __init__(self, picture):
        self.picture = picture

    def upload_picture_to_cloudinary(self):

        cloudinary.config(
            cloud_name=config("CLOUD_NAME"),
            api_key=config("CLOUD_API_KEY"),
            api_secret=config("CLOUD_API_SECRET"),
        )
        upload_result = None

        file_to_upload = self.picture
        if file_to_upload:
            upload_result = cloudinary.uploader.upload(
                file_to_upload,
                folder="parking",
            )
            return upload_result["url"]
        return False
