from rest_framework.permissions import IsAuthenticated

from .permissions import IsStaffEditorPermission

class StaffEditorPermissionMixin():
    permission_classes = [IsAuthenticated]