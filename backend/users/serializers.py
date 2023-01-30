from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

from .models import User
from .validators import unique_email_validator
from .components import UserCommonComponents

class UserSerializer(serializers.ModelSerializer): 
    email = serializers.EmailField(validators=[unique_email_validator])
    first_name = serializers.CharField(max_length=20, required=True)
    last_name = serializers.CharField(max_length=20, required=True)
    avatar = serializers.URLField(required=False)

    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "avatar",
            "email",
        )
    
class UserResponse(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'id', 'avatar')

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[unique_email_validator])
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    
    class Meta:
        model = User
        fields = ('username', 'password',
            'email', 'first_name', 'last_name')

        extra_kwargs = {
        'first_name': {'required': True},
        'last_name': {'required': True}
        }

    def create(self, validated_data):
        return UserCommonComponents.createUse(validated_data=validated_data)