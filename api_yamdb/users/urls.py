from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, TokenObtainPairView, UserSignUpView

router = DefaultRouter()

router.register('v1/users', UserViewSet, basename='users')
urlpatterns = [
    path('', include(router.urls)),
    path(
        'v1/auth/token/', TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    path(
        'v1/auth/signup/', UserSignUpView.as_view(),
        name='sign_up'
    ),
]
