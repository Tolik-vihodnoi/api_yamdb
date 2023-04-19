import datetime

from rest_framework.exceptions import ValidationError
from django.db.models import Avg

from reviews.models import Category, Genre, GenreTitle, Title, Comment, Review
from users.models import User
from rest_framework import serializers, validators
from rest_framework.relations import SlugRelatedField


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
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year',
                  'rating', 'description', 'genre', 'category')

    def validate_year(self, value):
        if value > datetime.date.today().year:
            raise ValidationError("Год произведения не может быть больше"
                                  "текущего года")
        return value


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для отзывов к произведениям."""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    class Meta:
        exclude = ('title',)
        read_only_fields = ('pub_date',)
        model = Review

    def validate(self, data):
        """Запрет публикации только одного отзыва на каждое произведение."""
        if self.context['request'].method != 'POST':
            return data
        title_id = self.context['view'].kwargs.get('title_id')
        author = self.context['request'].user
        review = Review.objects.filter(
            author=author, title=title_id
        )
        if review.exists():
            raise serializers.ValidationError(
                'На каждое произведение можно опубликовать только один отзыв.'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для комментариев к отзывам."""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    class Meta:
        exclude = ('review',)
        read_only_fields = ('review', 'pub_date')
        model = Comment
