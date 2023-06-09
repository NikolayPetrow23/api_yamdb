# Generated by Django 3.2 on 2023-04-25 15:53

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import reviews.validators


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'name',
                    models.CharField(
                        max_length=200, verbose_name='имя категории'
                    ),
                ),
                (
                    'slug',
                    models.SlugField(
                        unique=True, verbose_name='слаг категории'
                    ),
                ),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'name',
                    models.CharField(max_length=200, verbose_name='имя жанра'),
                ),
                (
                    'slug',
                    models.SlugField(unique=True, verbose_name='cлаг жанра'),
                ),
            ],
            options={
                'verbose_name': 'Жанр',
                'verbose_name_plural': 'Жанры',
            },
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'name',
                    models.CharField(
                        db_index=True, max_length=200, verbose_name='название'
                    ),
                ),
                (
                    'year',
                    models.IntegerField(
                        validators=[reviews.validators.validate_year],
                        verbose_name='год',
                    ),
                ),
                (
                    'description',
                    models.TextField(
                        blank=True,
                        max_length=255,
                        null=True,
                        verbose_name='описание',
                    ),
                ),
                (
                    'category',
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name='titles',
                        to='reviews.category',
                        verbose_name='категория',
                    ),
                ),
                (
                    'genre',
                    models.ManyToManyField(
                        related_name='titles',
                        to='reviews.Genre',
                        verbose_name='жанр',
                    ),
                ),
            ],
            options={
                'verbose_name': 'Произведение',
                'verbose_name_plural': 'Произведения',
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('text', models.TextField()),
                (
                    'score',
                    models.PositiveSmallIntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(
                                1, 'Не может быть меньше 1'
                            ),
                            django.core.validators.MaxValueValidator(
                                10, 'Не может быть больше 10'
                            ),
                        ]
                    ),
                ),
                (
                    'pub_date',
                    models.DateTimeField(
                        auto_now_add=True,
                        db_index=True,
                        verbose_name='Дата добавления',
                    ),
                ),
                (
                    'author',
                    models.ForeignKey(
                        default=1,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='reviews',
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    'title',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='reviews',
                        to='reviews.title',
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('text', models.TextField(verbose_name='Текст комментария')),
                (
                    'pub_date',
                    models.DateTimeField(
                        auto_now_add=True,
                        verbose_name='Дата публикации комментария',
                    ),
                ),
                (
                    'author',
                    models.ForeignKey(
                        default=1,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='comments',
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    'review',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='comments',
                        to='reviews.review',
                        verbose_name='Отзыв',
                    ),
                ),
            ],
        ),
        migrations.AddConstraint(
            model_name='review',
            constraint=models.UniqueConstraint(
                fields=('title', 'author'), name='title_author'
            ),
        ),
    ]
