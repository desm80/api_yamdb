import secrets
from smtplib import SMTPResponseException

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db import IntegrityError
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenViewBase

from .permissions import IsAdmin
from .serializers import UserSerializer, TokenObtainPairSerializer, \
    UserSignUpSerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAdmin,)
    page_number = 5
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^username',)

    @action(methods=['patch', 'get'],
            permission_classes=[IsAuthenticated],
            detail=False)
    def me(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.get_serializer(user)
        if self.request.method == 'PATCH':
            serializer = self.get_serializer(
                user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            if user.is_user and request.data.get('role') != 'User':
                return Response(serializer.data)
            serializer.save()
        return Response(serializer.data)


class TokenObtainPairView(TokenViewBase):
    serializer_class = TokenObtainPairSerializer


class UserSignUpView(CreateAPIView):
    serializer_class = UserSignUpSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = secrets.token_urlsafe()
        try:
            user = User.objects.get_or_create(
                email=serializer.data.get('email'),
                username=serializer.data.get('username'),
            )[0]
        except IntegrityError:
            return Response(
                data={
                    'error': 'Код подтверждения отправлен на e-mail!',
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        user.confirmation_code = token
        user.save()
        message = (
            f'Код подтверждения для продолжения регистрации - {token}'
        )

        try:
            send_mail(
                subject='Регистрация на сайте',
                message=message,
                from_email=settings.MAILING_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        except SMTPResponseException:
            user.delete()
            return Response(
                data={
                    'error': 'Ошибка отправки кода подтверждения!',
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
