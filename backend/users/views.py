from django.contrib.auth import login

from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView
from knox.models import AuthToken
from rest_framework import viewsets, generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.decorators import api_view

from .mixins import UserViewSetPermissionMixin
from .models import User
from .serializers import UserSerializer, RegisterSerializer, UserWithSlidesSerializer
from .views_components import ViewsCommonComponents


class UserViewSet(UserViewSetPermissionMixin, viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        query_params = request.GET.get('slides')

        if query_params:
            self.serializer_class = ViewsCommonComponents.check_include_slides_params(
                query_params)
        else:
            self.serializer_class = UserSerializer

        return super().list(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        self.check_object_permissions(request, instance)
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)

        if serializer.is_valid(raise_exception=True):
            serializer.save(avatar=serializer.validated_data.get('avatar'))
            return Response({
                "status_code": 200,
                "message": "success",
                "data": serializer.data
            }, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        self.check_object_permissions(request, instance)
        self.serializer_class = UserWithSlidesSerializer
        return super().retrieve(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.check_object_permissions(request, instance)
        return super().destroy(request, *args, **kwargs)

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = (AllowAny,)
        elif self.action == 'create':
            permission_classes = (IsAuthenticated,)
        else:
            permission_classes = self.permission_classes

        return [permission() for permission in permission_classes]


class RegisterUserAPIView(generics.GenericAPIView):
    permission_classes = (AllowAny, )
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        return Response({
            "status_code": 200,
            "message": "success",
            "data": UserSerializer(user).data,
            "token": AuthToken.objects.create(user)[1],
        }, status=status.HTTP_200_OK)


class LogInAPIView(KnoxLoginView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LogInAPIView, self).post(request, format=None)

    def get_post_response_data(self, request, token, instance):
        query_params = request.query_params.get('slides')

        if query_params is not None:
            serializer = ViewsCommonComponents.check_include_slides_params(
                query_params)
        else:
            serializer = self.get_user_serializer_class()

        query_set = User.objects.filter(username=request.user).values(
            'id', 'username', 'first_name', 'last_name', 'email', 'avatar', 'slides_info')[0]
        user_data = UserSerializer(query_set).data

        data = {
            'users': user_data,
            'expiry': self.format_expiry_datetime(instance.expiry),
            'token': token
        }
        if serializer is not None:
            data["users"] = serializer(
                request.user,
                context=self.get_context()
            ).data
        return data


@api_view(['POST'])
def authenticate_token(request):
    token = request.META.get('HTTP_AUTHORIZATION').split(
    )[1] if 'HTTP_AUTHORIZATION' in request.META else None

    if not token:
        return Response({'error': 'Token not provided'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        token_payload = AuthToken.objects.get(token_key=token[:8])
        username = str(token_payload).split(' ')[2]
        query_set = User.objects.get(username=username)
        user_info = UserSerializer(query_set).data
        return Response({
            "status_code": 200,
            "message": "success",
            "user": user_info
        }, status=status.HTTP_200_OK)

    except AuthToken.DoesNotExist:
        return Response({
            "status_code": 401,
            "error": "invalid token"
        }, status=status.HTTP_401_UNAUTHORIZED)


register_generic_view = RegisterUserAPIView.as_view()
login_generic_view = LogInAPIView.as_view()
