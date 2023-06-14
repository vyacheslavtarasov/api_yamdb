from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from reviews.models import Titles, User
from reviews.models import Review

from rest_framework.pagination import PageNumberPagination
from api.serializers import (
    ReviewSerializer,
)


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
