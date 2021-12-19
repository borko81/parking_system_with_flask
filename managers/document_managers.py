import datetime
import os

from botocore.exceptions import ClientError
from werkzeug.exceptions import BadRequest, InternalServerError

from constants import TEMP_FILE_FOLDER
from helpers.data_preparation import data_preparate_for_commit
from helpers.decode_document import decode_file
from models.documents import ParkingDocumentsModel
from schemas.response.document_response import DocResponse
from services.s3service import S3Service

s3 = S3Service()


class DocumentManaagers:
    """
    After decode string, save file in temporary folder, drom where, begin procedure to
    upload to amazon. If everything is ok, delete this file from temp. url return from s3 save in
    document model.
    """

    @staticmethod
    def upload_doc(data):
        encoded_data = data["ecoded_string"]
        extension = data["ext"]
        name_ext = str(datetime.datetime.now()).split()[0]
        name_doc = f"{data['name']}-{name_ext}.{extension}"
        path = os.path.join(TEMP_FILE_FOLDER, f"{name_doc}")
        decode_file(path, encoded_data)
        try:
            url = s3.upload_file(path, name_doc)
        except ClientError:
            raise InternalServerError(
                "Provider is not available at the moment. " "Please try again later"
            )
        except Exception:
            raise BadRequest("Error with try to upload to aws")
        else:
            try:
                document = ParkingDocumentsModel(name=data["name"], url=url)
                data_preparate_for_commit(document)
            except Exception:
                raise BadRequest("Error when try to save data in database")
        finally:
            os.remove(path)

    @staticmethod
    def get_doc():
        schema = DocResponse()
        return schema.dump(ParkingDocumentsModel.query.all(), many=True)
