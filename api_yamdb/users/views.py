from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from .models import User
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.username = validated_data.get('username', instance.username)
        instance.user.role = validated_data.get('role', instance.user.role)
        instance.save()
        return instance




