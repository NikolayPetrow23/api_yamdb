import re
from typing import Any

from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_username(value: Any) -> Any:
    if value == 'me':
        raise ValidationError(
            ('Имя пользователя не может быть <me>.'),
            params={'value': value},
        )
    if re.search(r'^[a-zA-Z][a-zA-Z0-9-_\.]{1,20}$', value) is None:
        raise ValidationError(
            (f'Не допустимые символы <{value}> в нике.'),
            params={'value': value},
        )
    return value


def validate_year(value: Any) -> None:
    now = timezone.now().year
    if value > now:
        raise ValidationError(f'{value} не может быть больше {now}')
