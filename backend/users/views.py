from rest_framework import viewsets
from .models import User
from .serializers import UserSerializer
from authentication.mixins import StaffEditorPermissionMixin
from rest_framework import permissions

class UserViewSet(StaffEditorPermissionMixin, viewsets.ModelViewSet):

    permission_class = [permissions.IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer