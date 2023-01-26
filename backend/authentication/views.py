from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.contrib.auth import login
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView

from users.serializers import RegisterSerializer
from users.serializers import UserSerializer as RegisteredUserSerializer
from users.models import User

class RegisterUserAPIView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs): 
        serializer = self.get_serializer(data=request.data)   
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
    
        return Response ({
            "status": 200,
            "message": 'success',
            "data": {
                "user": RegisteredUserSerializer(user).data,
                "token": AuthToken.objects.create(user)[1],
            }
        })



class LogInAPIView(KnoxLoginView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = AuthTokenSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LogInAPIView, self).post(request, format=None)


    def get_post_response_data(self, request, token, instance):
        UserSerializer = self.get_user_serializer_class()

        query_set = User.objects.filter(username=request.user).values('id','username','first_name','last_name', 'email', 'avatar')[0]
        user_data = RegisteredUserSerializer(query_set).data

        data = {
            'users': user_data,
            'expiry': self.format_expiry_datetime(instance.expiry),
            'token': token
        }
        if UserSerializer is not None:
            data["user"] = UserSerializer(
                request.user,
                context=self.get_context()
            ).data
        return data



register_generic_view = RegisterUserAPIView.as_view()
login_generic_view = LogInAPIView.as_view()