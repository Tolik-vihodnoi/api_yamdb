from django.core.exceptions import ValidationError


def score_validation(score):
    if score not in range(1, 11):
        raise ValidationError('Введите число от 1 до 10!')
