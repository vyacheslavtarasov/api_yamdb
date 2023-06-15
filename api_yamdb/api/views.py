# from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from rest_framework import viewsets, status
from rest_framework.filters import SearchFilter
from rest_framework.decorators import api_view
from rest_framework.response import Response
# from rest_framework.views import APIView
from authorization.send_confirmation_code import send_mail_code

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
    SignUpSerializer
)
# from .permissions import IsAdminUserOrReadOnly


@api_view(['POST'])
def signup_cust(request):
    """Регистрация пользователя."""
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data['email']
    username = serializer.validate_data['username']
    try:
        user = User.objects.get_or_create(
            email=email,
            username=username,
        )
    except IntegrityError:
        return Response(
            'Такой логин или @email уже заняты! Ввведите другой.',
            status=status.HTTP_400_BAD_REQUEST
        )
    user.confirmation_code = send_mail_code(request.data)
    user.save()
    return Response(serializer.data, status=status.HTTP_200_OK)


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
