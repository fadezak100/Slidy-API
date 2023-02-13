from .serializers import UserWithSlidesSerializer, UserSerializer

from .models import User
from .serializers import UserSerializer
from knox.models import AuthToken


class ViewsCommonComponents:

    def assign_new_serializer(query_params):
        include_slide = True if query_params.lower() == 'true' else False
        serializer = UserSerializer

        if include_slide:
            serializer = UserWithSlidesSerializer

        return serializer

    def authenticate_token(headers):
        token = headers.get('HTTP_AUTHORIZATION').split(
        )[1] if 'HTTP_AUTHORIZATION' in headers else None

        token_payload = AuthToken.objects.get(token_key=token[:8])
        username = str(token_payload).split(' ')[2]
        query_set = User.objects.get(username=username)
        user_info = UserSerializer(query_set).data
        return user_info
