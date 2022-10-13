from api.serializers import ReviewSerializer, CommentSerializer
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import viewsets


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = ...
    pagination_class = LimitOffsetPagination
    # допилить методы


class CommentViewSer(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = ...
    pagination_class = LimitOffsetPagination
    # допилить методы
