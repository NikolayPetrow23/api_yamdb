from typing import Any

from rest_framework import serializers

from reviews.validators import validate_username as valid_username
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )


class ProfileSerializer(serializers.ModelSerializer):
    class Meta(UserSerializer.Meta):
        read_only_fields = ('role',)


class SignUpUserSerializer(serializers.ModelSerializer):
    def validate_username(self, username: Any) -> Any:
        return valid_username(username)

    class Meta:
        model = User
        fields = ('email', 'username')


class MyAuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()
