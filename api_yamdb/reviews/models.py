from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from reviews.validators import validate_year
from users.models import User


class BaseModel(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        default=1,
    )

    class Meta:
        abstract = True


class Category(models.Model):
    name = models.CharField('имя', max_length=200)
    slug = models.SlugField('слаг', unique=True, db_index=True)

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self) -> str:
        return {self.name}


class Genre(models.Model):
    name = models.CharField('имя', max_length=200)
    slug = models.SlugField('cлаг', unique=True, db_index=True)

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'жанры'

    def __str__(self) -> str:
        return f'{self.name} {self.name}'


class Title(models.Model):
    name = models.CharField('название', max_length=200, db_index=True)
    year = models.IntegerField('год', validators=(validate_year,))
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='категория',
        null=True,
        blank=True,
    )
    description = models.TextField(
        'описание',
        max_length=255,
        blank=True,
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='жанр',
    )

    class Meta:
        verbose_name = 'произведение'
        verbose_name_plural = 'произведения'

    def __str__(self) -> str:
        return self.name


class Review(BaseModel):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    text = models.TextField()
    score = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1, 'Не может быть меньше 1'),
            MaxValueValidator(10, 'Не может быть больше 10'),
        ],
    )
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('title', 'author'),
                name='title_author',
            ),
        ]

    def __str__(self) -> str:
        return self.text


class Comments(BaseModel):
    review = models.ForeignKey(
        Review,
        verbose_name='Отзыв',
        related_name='comments',
        on_delete=models.CASCADE,
    )
    text = models.TextField(verbose_name='Текст комментария')
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации комментария',
        auto_now_add=True,
    )

    def __str__(self) -> str:
        return self.text
