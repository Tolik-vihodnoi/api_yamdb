from rest_framework.exceptions import ValidationError
from django.core.validators import RegexValidator

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
