from flask import request
from flask_restful import Resource

from helpers.decorator import validate_schema, permission_required
from managers.auth import auth
from managers.document_managers import DocumentManaagers
from models import UserType
from schemas.request.doc_request import DocRequest


class DocumentResourse(Resource):
    @auth.login_required
    @permission_required(UserType.admin)
    def get(self):
        return DocumentManaagers.get_doc()


    @auth.login_required
    @permission_required(UserType.admin)
    @validate_schema(DocRequest)
    def post(self):
        data = request.get_json()
        return DocumentManaagers.upload_doc(data), 201