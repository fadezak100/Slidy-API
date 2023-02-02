from rest_framework import serializers

from users.models import User
from .models import Slide

from django.core.validators import FileExtensionValidator


class UserSlideInlineSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    first_name = serializers.CharField(max_length=20)
    last_name = serializers.CharField(max_length=20)
    avatar = serializers.URLField()
    email = serializers.EmailField()

class SlideSerializer(serializers.ModelSerializer):
    title = serializers.CharField(allow_null=True)
    user_data = serializers.SerializerMethodField(read_only=True)
    slide = serializers.FileField(write_only=True, validators=[FileExtensionValidator(['md'], 'only .md files are allowed')])
    is_public = serializers.BooleanField(default=True)
    is_live = serializers.BooleanField(default=False)

    class Meta:
        model = Slide
        fields = (
            'id',
            'user_data',
            'title',
            'url',
            'description',
            'is_public',
            'is_live',
            'slide',
        )

    def get_user_data(self, obj):
        return UserSlideInlineSerializer(obj.user).data