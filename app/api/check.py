from flask_restx import Resource
from app.api import check_api
from app.helpers.auth import require_auth
from app.helpers.api_response import BaseApiResponse

@check_api.route('/')
class List(Resource):

    @require_auth
    def get(self):
        res = BaseApiResponse()
        return res.make()
