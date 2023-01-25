from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = User
        fields = (
            "id",
            "full_name",
            "first_name",
            "last_name",
            "avatar",
            "email",

        )

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
