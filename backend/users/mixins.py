from rest_framework.permissions import IsAuthenticated

from .permissions import IsOwnerPermission

class UserViewSetPermissionMixin:
    permission_classes = [IsAuthenticated, IsOwnerPermission]
