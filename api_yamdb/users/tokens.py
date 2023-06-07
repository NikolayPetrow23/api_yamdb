from typing import Dict

from django.contrib.auth.tokens import default_token_generator
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User


def get_tokens_for_user(user: User) -> Dict:
    access = RefreshToken.for_user(user)
    return {'access': str(access.access_token)}


def check_token(username: str, confirmation_code: str) -> bool:
    user = User.objects.get(username=username)
    if default_token_generator.check_token(user, confirmation_code):
        return True
