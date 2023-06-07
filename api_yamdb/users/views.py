from typing import Any, Tuple

from rest_framework import filters, generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User
from users.paginator import CustomPagination
from users.permissions import IsAdmin
from users.send_email_code import send_email_code
from users.serializers import (
    MyAuthTokenSerializer,
    ProfileSerializer,
    SignUpUserSerializer,
    UserSerializer,
)
from users.tokens import check_token, get_tokens_for_user


class SignUpViewSet(APIView):
    serializer_class = SignUpUserSerializer
    permission_classes = (AllowAny,)

    def post(self, request: Request) -> Response:
        email = request.data.get('email')
        username = request.data.get('username')
        serializer = SignUpUserSerializer(data=request.data)
        msg = {'messages': 'Такой пользователь уже существует'}
        if User.objects.filter(username=username, email=email).exists():
            user = User.objects.get(username=username)
            send_email_code(user)
            return Response(msg, status=status.HTTP_200_OK)
        serializer.is_valid(raise_exception=True)
        user = User.objects.create_user(email=email, username=username)
        send_email_code(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ConfirmationTokenView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = MyAuthTokenSerializer

    def post(
        self,
        request: Request,
        *args: Tuple[Any, ...],
        **kwargs: Tuple[Any, ...],
    ) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        confirmation_code = serializer.data.get('confirmation_code')
        username = serializer.data.get('username')
        user = get_object_or_404(User, username=username)

        if check_token(user, confirmation_code):
            return Response(
                get_tokens_for_user(user),
                status=status.HTTP_200_OK,
            )
        return Response(
            {'detail': 'Неверный confirmation token'},
            status=status.HTTP_400_BAD_REQUEST,
        )


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('role')
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    pagination_class = CustomPagination
    lookup_field = 'username'
    http_method_names = ('get', 'patch', 'delete', 'post')
    permission_classes = (IsAdmin,)

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=[IsAuthenticated],
        serializer_class=ProfileSerializer,
    )
    def me(self, request: Request) -> Response:
        user = self.request.user
        serializer = self.get_serializer(user)
        if request.method == 'PATCH':
            serializer = self.get_serializer(
                user,
                data=request.data,
                partial=True,
            )
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer.save(role=self.request.user.role))
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data, status.HTTP_200_OK)
