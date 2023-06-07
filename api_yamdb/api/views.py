from django.db.models import Avg, QuerySet
from django.shortcuts import get_object_or_404
from django.utils.functional import cached_property
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet

from api.filters import TitleFilter
from api.mixins import CreateListDestroyModelViewSet
from api.serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleReadSerializer,
    TitleWriteSerializer,
)
from reviews.models import Category, Comments, Genre, Review, Title
from users.paginator import CustomPagination
from users.permissions import (
    AuthUserAdminModeratorPermission,
    IsAdmin,
    ReadOnly,
)


class CategoryViewSet(CreateListDestroyModelViewSet):
    """Получить список всех категорий. Права доступа: Доступно без токена."""

    queryset = Category.objects.all().order_by('name')

    filter_backends = (SearchFilter,)
    lookup_field = 'slug'
    pagination_class = CustomPagination
    permission_classes = [ReadOnly | IsAdmin]
    search_fields = ('name',)
    serializer_class = CategorySerializer


class GenreViewSet(CreateListDestroyModelViewSet):
    """Получить список всех жанров. Права доступа: Доступно без токена."""

    queryset = Genre.objects.all().order_by('name')

    filter_backends = (SearchFilter,)
    lookup_field = 'slug'
    pagination_class = CustomPagination
    permission_classes = [ReadOnly | IsAdmin]
    search_fields = ('name',)
    serializer_class = GenreSerializer


class TitleViewSet(ModelViewSet):
    """Получить список всех объектов. Права доступа: Доступно без токена."""

    queryset = (
        Title.objects.annotate(rating=Avg('reviews__score'))
        .all()
        .order_by('name')
    )

    pagination_class = CustomPagination
    permission_classes = [ReadOnly | IsAdmin]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self) -> TitleWriteSerializer:
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleWriteSerializer


class ReviewViewSet(ModelViewSet):
    pagination_class = CustomPagination
    permission_classes = (AuthUserAdminModeratorPermission,)
    serializer_class = ReviewSerializer

    @cached_property
    def get_title(self) -> Title:
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self) -> QuerySet:
        return self.get_title.reviews.all().order_by('pub_date')

    def perform_create(self, serializer: ReviewSerializer) -> None:
        serializer.save(author=self.request.user, title=self.get_title)


class CommentViewSet(ModelViewSet):
    pagination_class = CustomPagination
    permission_classes = (AuthUserAdminModeratorPermission,)
    serializer_class = CommentSerializer

    @cached_property
    def get_review(self) -> Review:
        return get_object_or_404(Review, pk=self.kwargs.get('review_id'))

    def get_queryset(self) -> QuerySet:
        return Comments.objects.filter(review_id=self.get_review.id).order_by(
            'pub_date',
        )

    def perform_create(self, serializer: CommentSerializer) -> None:
        serializer.save(author=self.request.user, review_id=self.get_review.id)
