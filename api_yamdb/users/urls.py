from django.urls import include, path
from rest_framework import routers

from users import views

app_name = 'users'

router = routers.DefaultRouter()
router.register('users', views.UserViewSet, basename='users')


urlpatterns = [
    path(
        'v1/',
        include(
            [
                path('', include(router.urls)),
                path(
                    'auth/token/',
                    views.ConfirmationTokenView.as_view(),
                    name='token_obtain_pair',
                ),
                path(
                    'auth/signup/',
                    views.SignUpViewSet.as_view(),
                    name='signup',
                ),
            ],
        ),
    ),
]
