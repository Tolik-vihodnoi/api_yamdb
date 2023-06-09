from smtplib import SMTPResponseException

from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import Token

from reviews.models import Category, Genre, Review, Title
from users.models import User
from .filters import TitleFilter
from .permissions import IsAdminModeratorAuthor, IsAdminOrReadOnly, IsAdminUser
from .serializers import (CategorySerializer, CommentSerializer,
                          CreateTokenSerializer, CreateUserSerializer,
                          GenreSerializer, ReviewSerializer, TitleSerializer,
                          UserSerializer)


class GetPostPatchDelModelViewSet(viewsets.ModelViewSet):
    http_method_names = ('get', 'post', 'patch', 'delete')


class UserViewSet(GetPostPatchDelModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    @action(
        detail=False,
        methods=('GET', 'PATCH'),
        permission_classes=[IsAuthenticated],
    )
    def me(self, request):
        if request.method == 'GET':
            serialiser = UserSerializer(request.user)
            return Response(serialiser.data)

        serialiser = UserSerializer(request.user, request.data, partial=True)
        serialiser.is_valid(raise_exception=True)
        serialiser.save(role=request.user.role)
        return Response(serialiser.data)


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    """Создание нового пользователя."""
    serializer = CreateUserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data.get('email')
    user, _ = User.objects.get_or_create(**serializer.validated_data)
    token = default_token_generator.make_token(user)
    try:
        send_mail(
            'confirmation code',
            token,
            settings.MAILING_EMAIL,
            [email],
            fail_silently=False,
        )
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    except SMTPResponseException:
        user.delete()
        return Response(
            data={'error': 'Ошибка отправки кода!'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def create_token(request):
    """Создание токена для пользователей."""
    serializer = CreateTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User,
        username=serializer.validated_data.get('username')
    )
    confirmation_code = serializer.validated_data.get('confirmation_code')

    if default_token_generator.check_token(user, confirmation_code):
        jwt_token = Token.for_user(user)
        return Response(
            {'token': f'{jwt_token}'}, status=status.HTTP_200_OK
        )
    return Response(
        {'message': 'Нет доступа'},
        status=status.HTTP_400_BAD_REQUEST
    )


class CustomCrDelListViewSet(mixins.CreateModelMixin,
                             mixins.DestroyModelMixin,
                             mixins.ListModelMixin,
                             viewsets.GenericViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('$name',)
    lookup_field = 'slug'
    lookup_value_regex = r'[-a-zA-Z0-9_]{,50}'


class CategoryViewSet(CustomCrDelListViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CustomCrDelListViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(GetPostPatchDelModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')).order_by('name', 'category')
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly, )
    filter_backends = (DjangoFilterBackend, )
    filterset_class = TitleFilter


class CommentViewSet(GetPostPatchDelModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAdminModeratorAuthor,)

    def get_queryset(self):
        review_id = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'),
            title=self.kwargs.get('title_id'),
        )
        return review_id.comments.all()

    def perform_create(self, serializer):
        review_id = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'),
            title=self.kwargs.get('title_id'),
        )
        serializer.save(author=self.request.user, review_id=review_id)


class ReviewViewSet(GetPostPatchDelModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAdminModeratorAuthor,)

    def get_queryset(self):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)
