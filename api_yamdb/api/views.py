from django.shortcuts import get_object_or_404
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view, action
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response

from reviews.models import Category, Genre, Title
from api.paginator import CommentPagination
from api.filters import TitleFilter
from api.serializers import (CategoriesSerializer,
                             CommentsSerializer, GenresSerializer,
                             ReviewsSerializer,
                             TitlesSerializer, TitlesViewSerializer)



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    permission_classes = (OwnerOrAdmins, )
    filter_backends = (filters.SearchFilter, )
    filterset_fields = ('username')
    search_fields = ('username', )
    lookup_field = 'username'

    @action(
        methods=['get', 'patch'],
        detail=False,
        url_path='me',
        permission_classes=(IsAuthenticated, )
    )
    def get_patch_me(self, request):
        user = get_object_or_404(User, username=self.request.user)
        if request.method == 'GET':
            serializer = MeSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == 'PATCH':
            serializer = MeSerializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    serializer_class = TitlesSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = PageNumberPagination
    filterset_class = TitleFilter
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TitlesViewSerializer
        return TitlesSerializer


class ReviewGenreModelMixin(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsAdminOrReadOnly
    ]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'slug')
    lookup_field = 'slug'


class CategoriesViewSet(ReviewGenreModelMixin):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer


class GenresViewSet(ReviewGenreModelMixin):
    queryset = Genre.objects.all()
    serializer_class = GenresSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewsSerializer
    pagination_class = CommentPagination
    permission_classes = [AuthorAndStaffOrReadOnly]

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        new_queryset = title.reviews.all()
        return new_queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer
    pagination_class = CommentPagination
    permission_classes = [AuthorAndStaffOrReadOnly]

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        try:
            review = title.reviews.get(id=self.kwargs.get('review_id'))
        except TypeError:
            TypeError('У произведения нет такого отзыва')
        queryset = review.comments.all()
        return queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        try:
            review = title.reviews.get(id=self.kwargs.get('review_id'))
        except TypeError:
            TypeError('У произведения нет такого отзыва')
        serializer.save(author=self.request.user, review=review)
