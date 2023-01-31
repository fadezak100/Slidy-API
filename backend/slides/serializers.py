from rest_framework import serializers

from users.models import User
from .models import Slide

class UserSlideInlineSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    first_name = serializers.CharField(max_length=20)
    last_name = serializers.CharField(max_length=20)
    avatar = serializers.URLField()
    email = serializers.EmailField()

class SlideSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=200)
    user_data = serializers.SerializerMethodField(read_only=True)

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
        )

    def validate_title(self, value):
        if value == '':
            raise  serializers.ValidationError("Title can't be blank")
        return value

    def get_user_data(self, obj):
        return UserSlideInlineSerializer(obj.user).data