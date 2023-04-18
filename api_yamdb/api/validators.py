from rest_framework.exceptions import ValidationError
from django.core.validators import RegexValidator
from users.models import User

username_validator = RegexValidator(r'^[\w.@+-]+$',
                                    'Имя пользователя должно содержать только'
                                    'буквы, цифры или следующие символы:'
                                    ' @ . + - _',
                                    'invalid'
                                    )


def validate_username(username):
    if username == 'me':
        raise ValidationError(
            "Использовать имя 'me' в качестве username запрещено!"
        )
    if User.objects.filter(username=username).exists():
        raise ValidationError('Пользователь с таким именем '
                              'уже зарегестрирован')


def validate_email(email):
    if User.objects.filter(email=email).exists():
        raise ValidationError('Пользователь с такой почтой '
                              'уже зарегестрирован')
