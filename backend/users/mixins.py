from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .permissions import IsOwnerPermission

class UserViewSetPermissionMixin:
    permission_classes = [IsAuthenticated, IsOwnerPermission]