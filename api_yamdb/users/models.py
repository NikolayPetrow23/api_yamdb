from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    class RoleUser(models.TextChoices):
        user = 'user', _('Аутентифицированный пользователь')
        moderator = 'moderator', _('Модераторoр')
        admin = 'admin', _('Администратор')

    email = models.EmailField(unique=True, max_length=254)
    role = models.CharField(
        max_length=9, default=RoleUser.user, choices=RoleUser.choices,
    )
    bio = models.TextField('Биография', blank=True)
