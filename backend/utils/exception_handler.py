from rest_framework.response import Response

from rest_framework.views import exception_handler
from .generic_errors import SlideRequestError, UploadSlidesError


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

        if isinstance(exc, SlideRequestError):
            response['message'] = str(exc)
            response['status_code'] = 500

        if isinstance(exc, UploadSlidesError):
            response['message'] = str(exc)
            response['status_code'] = 500

        if isinstance(exc, TypeError):
            response['message'] = str(exc)
            response['status_code'] = 500

        return Response(response)
