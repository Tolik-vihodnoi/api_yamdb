from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework.exceptions import ValidationError
from django.db import models

username_validator = UnicodeUsernameValidator()


def validate_username(username):
    if username == 'me':
        raise ValidationError(
            "Использовать имя 'me' в качестве username запрещено!"
        )


class User(AbstractUser):
    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'

    CHOISES = (
        (ADMIN, 'Администратор'),
        (USER, 'Аутентифицированный пользователь'),
        (MODERATOR, 'Модератор'),
    )

    username = models.CharField(
        'username',
        max_length=150,
        unique=True,
        validators=[username_validator, validate_username],
    )

    email = models.EmailField(unique=True)

    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField('Роль', max_length=20,
                            choices=CHOISES, default='user')

    class Meta:
        ordering = ('email',)

    @property
    def is_moderator(self):
        return self.role == User.MODERATOR

    @property
    def is_admin(self):
        return self.role == User.ADMIN or (self.is_staff or self.is_superuser)
