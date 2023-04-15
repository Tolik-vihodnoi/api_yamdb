from reviews.models import Category, Genre
from users.models import User
from rest_framework import serializers, validators

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
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role', )


class CategorySerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(
        max_length=50,
        validators=[validators.UniqueValidator(Category.objects.all())]
    )

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')
