import cloudinary
import cloudinary.uploader
from decouple import config


def upload_picture_to_cloudinary(picture):

    cloudinary.config(
        cloud_name=config("CLOUD_NAME"),
        api_key=config("CLOUD_API_KEY"),
        api_secret=config("CLOUD_API_SECRET"),
    )
    upload_result = None

    file_to_upload = picture
    if file_to_upload:
        upload_result = cloudinary.uploader.upload(
            file_to_upload,
            folder="parking",
        )
        return upload_result["url"]
    return False
