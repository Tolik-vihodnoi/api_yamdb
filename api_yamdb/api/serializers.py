from users.models import User
from rest_framework import serializers

class CreateUserSerializer(serializers.ModelSerializer):
    """Сериализатор создания нового пользователя."""

    class Meta:
        model = User
        fields = ('username', 'email',)


class CreateTokenSerializer(serializers.ModelSerializer):
    """Сериализатор создания токена."""
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    class Meta:
        model = User
        fields = ('username', 'confirmation_code',)

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role',)