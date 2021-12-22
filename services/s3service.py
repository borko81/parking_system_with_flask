import boto3
from botocore.exceptions import ClientError


from decouple import config
from werkzeug.exceptions import InternalServerError


class S3Service:
    def __init__(self):
        self.key = config("AWSAccessKeyId")
        self.secret = config("AWSSecretKey")
        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=self.key,
            aws_secret_access_key=self.secret,
        )
        self.bucket = config("AWS_BUCKET")

    def upload_file(self, path, key):
        try:
            self.s3.upload_file(
                path, self.bucket, key, ExtraArgs={"ACL": "public-read"}
            )
            return f"https://{config('AWS_BUCKET')}.s3.{config('AWS_REGION')}.amazonaws.com/{key}"
        except ClientError:
            raise InternalServerError("S3 is not available at the moment")
