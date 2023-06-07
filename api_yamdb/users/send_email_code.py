from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.urls import reverse

from users.models import User


def send_email_code(user: User) -> None:
    subject = f'Подтверждение учетной записи для {user.username}'
    link = settings.DOMAIN_NAME + reverse('users:token_obtain_pair')
    confirmation_code = default_token_generator.make_token(user)
    message = (
        f'Для подтверждения учетной записи для {user.username}, '
        f'сделайте запрос на эндпоинт: {link}'
        f'и введите код: {confirmation_code}'
    )
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email],
        fail_silently=False,
    )
