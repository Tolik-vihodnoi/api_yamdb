import datetime
from rest_framework.exceptions import ValidationError
from reviews.models import Category, Genre, GenreTitle, Title
from users.models import User
from .validators import validate_username, validate_email, username_validator
from rest_framework import serializers, validators


class CreateUserSerializer(serializers.ModelSerializer):
    """Сериализатор создания нового пользователя."""
    email = serializers.EmailField(max_length=254)
    username = serializers.CharField(max_length=150,
                                     validators=[username_validator])

    class Meta:
        model = User
        fields = ('username', 'email',)

    def validate_username(self, username):
        if username == 'me':
            raise ValidationError("Имя 'me' в качестве username запрещено!")
        return username


class CreateTokenSerializer(serializers.ModelSerializer):
    """Сериализатор создания токена."""
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    class Meta:
        model = User
        fields = ('username', 'confirmation_code',)


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=254, validators=[validate_email])
    username = serializers.CharField(max_length=150, validators=[
        validate_username, username_validator])

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role', )


class CustomSlugRelatedField(serializers.SlugRelatedField):

    def to_representation(self, obj):
        return {"name": obj.name, "slug": obj.slug}


class CategorySerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(
        max_length=50,
        validators=[validators.UniqueValidator(
            Category.objects.all(),
            message='Категория с таким slug уже существует'
        )]
    )

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(
        max_length=50,
        validators=[validators.UniqueValidator(
            Genre.objects.all(),
            message='Жанр с таким slug уже существует'
        )]
    )

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    genre = CustomSlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all()
    )
    category = CustomSlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description',
                  # 'rating',
                  'genre', 'category')

    def validate_year(self, value):
        if value > datetime.date.today().year:
            raise ValidationError("Год произведения не может быть больше"
                                  "текущего года")
        print("ЗАВАЛИДИРОВАЛИ ГОД")
        return value
