from smtplib import SMTPResponseException
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from .serializers import CreateTokenSerializer, CreateUserSerializer, UserSerializer
from users.models import User
from django.conf import settings
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .permissions import IsAdminUser


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'username'

    @action(
        detail=False,
        methods=(['GET', 'PATCH']),
        permission_classes=[IsAuthenticated],
    )
    def me(self, request):
        if request.method == 'GET':
            serialiser = UserSerializer(request.user)
            return Response(serialiser.data)


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    """Создание нового пользователя."""
    serializer = CreateUserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    email = serializer.validated_data.get('email')
    user, created = User.objects.get_or_create(username=username, email=email)
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
        jwt_token = RefreshToken.for_user(user)
        return Response(
            {'token': f'{jwt_token.access_token}'}, status=status.HTTP_200_OK
        )
    return Response(
        {'message': 'Нет доступа'},
        status=status.HTTP_400_BAD_REQUEST
    )
