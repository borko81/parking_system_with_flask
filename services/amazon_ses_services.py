import boto3
from botocore.exceptions import ClientError

from decouple import config
from werkzeug.exceptions import BadRequest


class SeSEmail:
    def send_email(self, message):

        AWS_REGION = "eu-central-1"
        AWS_S3_CREDS = {
            "aws_access_key_id": config("AWSAccessKeyId"),
            "aws_secret_access_key": config("AWSSecretKey"),
        }

        ses = boto3.client("ses", region_name=AWS_REGION, **AWS_S3_CREDS)

        body = f"{message}"

        try:
            ses.send_email(
                Source=config("GMAIL_ADDRESS"),
                Destination={"ToAddresses": [config("GMAIL_ADDRESS")]},
                Message={
                    "Subject": {"Data": "Message from park system", "Charset": "UTF-8"},
                    "Body": {"Text": {"Data": body, "Charset": "UTF-8"}},
                },
            )
        except ClientError as ex:
            raise BadRequest(str(ex))


if __name__ == "__main__":
    SeSEmail().send_email("check")
