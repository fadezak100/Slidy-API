from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView

from rest_framework import viewsets, permissions, generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.contrib.auth import login

from .mixins import StaffEditorPermissionMixin
from .models import User
from .serializers import UserSerializer, RegisterSerializer


class UserViewSet(StaffEditorPermissionMixin, viewsets.ModelViewSet):
    permission_class = [permissions.IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class RegisterUserAPIView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response({
            "status": 200,
            "message": "success",
            "data": {
                "user": self.get_serializer(user).data,
                "token": AuthToken.objects.create(user)[1]
            }
        })


class LogInAPIView(KnoxLoginView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = AuthTokenSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        request.user = user
        return super(LogInAPIView, self).post(request, format=None)

    def get_post_response_data(self, request, token, instance):
        serializer = self.get_user_serializer_class()

        query_set = \
        User.objects.filter(username=request.user).values('id', 'username', 'first_name', 'last_name', 'email',
                                                          'avatar')[0]
        user_data = UserSerializer(query_set).data

        data = {
            'users': user_data,
            'expiry': self.format_expiry_datetime(instance.expiry),
            'token': token
        }
        if serializer is not None:
            data["user"] = serializer(
                request.user,
                context=self.get_context()
            ).data
        return data


register_generic_view = RegisterUserAPIView.as_view()
login_generic_view = LogInAPIView.as_view()
