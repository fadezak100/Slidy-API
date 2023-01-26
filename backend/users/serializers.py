from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

from .models import User
from .validators import unique_email_validator


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
    email = serializers.EmailField(required=True, validators=[validate_email])
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
        user = User.objects.create(
        username=validated_data['username'],
        email=validated_data['email'],
        first_name=validated_data['first_name'],
        last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        user.save()

        return user