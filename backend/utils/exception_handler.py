from rest_framework.response import Response

from rest_framework.views import exception_handler
from .generic_errors import BaseException


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        response.data['status_code'] = response.status_code
        return response

    if response is None:
        response = {
            "message": str(exc),
            "status_code": 500,
        }

        if isinstance(exc, BaseException):
            response['message'] = exc.message
            response['status_code'] = exc.status

        return Response(response, status=response['status_code'])
