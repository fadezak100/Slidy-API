from .serializers import UserWithSlidesSerializer, UserSerializer


class ViewsCommonComponents:

    def check_include_slides_params(query_params):
        include_slide = True if query_params.lower() == 'true' else False

        if include_slide:
            serializer = UserWithSlidesSerializer
        else:
            serializer = UserSerializer

        return serializer
