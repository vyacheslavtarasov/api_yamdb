from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.filters import SearchFilter

from reviews.models import (
    Review,
    Comments,
    Titles,
    User,
    Genre,
)

from rest_framework.pagination import PageNumberPagination
from api.serializers import (
    ReviewSerializer,
    CommentsSerializer,
    GenreSerializer,
)
# from .permissions import IsAdminUserOrReadOnly


class ReviewsViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    pagination_class = PageNumberPagination 

    def get_queryset(self):
        new_queryset = Review.objects.filter(title_id=self.kwargs.get("title_id"))
        return new_queryset
    
    def perform_create(self, serializer):
        serializer.save(
            title_id=get_object_or_404(Titles, id=self.kwargs.get("title_id")),
            author=get_object_or_404(User, username=self.request.user),
        )

    def perform_update(self, serializer):
        serializer.save(
            title_id=get_object_or_404(Titles, id=self.kwargs.get("title_id")),
            author=get_object_or_404(User, username=self.request.user),
        )


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer

    pagination_class = PageNumberPagination 

    def get_queryset(self):
        print(self.kwargs.get("review_id"))
        new_queryset = Comments.objects.filter(review_id=self.kwargs.get("review_id"))
        return new_queryset
    
    def perform_create(self, serializer):
        serializer.save(
            review_id=get_object_or_404(Review, id=self.kwargs.get("review_id")),
            author=get_object_or_404(User, username=self.request.user),
        )

    def perform_update(self, serializer):
        serializer.save(
            review_id=get_object_or_404(Review, id=self.kwargs.get("review_id")),
            author=get_object_or_404(User, username=self.request.user),
        )


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    #permission_classes = (IsAdminUserOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name', )
    lookup_field = 'slug'
