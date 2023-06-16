import action
from rest_framework.decorators import action
# from django import views
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError

from rest_framework import (
    filters, viewsets, status, permissions)

from rest_framework.filters import SearchFilter
from api.permissions import IsAuthor

from rest_framework import viewsets, status
from rest_framework.pagination import PageNumberPagination

from rest_framework.filters import SearchFilter

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import AccessToken

from authorization.send_confirmation_code import send_mail_code

from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend


from api.permissions import (IsAuthor,
                             IsAdminOrReadOnly,
                             )

from reviews.models import (
    Review,
    Comments,
    Title,
    User,
    Genre,
    Category,
)

from rest_framework.pagination import PageNumberPagination
from api.serializers import (
    ReviewSerializer,
    CommentsSerializer,
    GenreSerializer,
    SignUpSerializer,
    CategorySerializer,
    TokenSerializer,
    TitleReadSerializer,
    TitleWriteSerializer,
    UserSerializer,
    UserMeSerializer,

)
# from .permissions import IsAdminUserOrReadOnly


@api_view(['POST'])
def signup_cust(request):
    """Регистрация пользователя."""
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    # email = serializer.validated_data['email']
    # username = serializer.validated_data['username']
    try:
        user, _ = User.objects.get_or_create(
            username=serializer.validated_data.get('username'),
            email=serializer.validated_data.get('email')
        )
    except IntegrityError:
        return Response(
            'Такой логин или @email уже заняты! Ввведите другой.',
            status=status.HTTP_400_BAD_REQUEST
        )
    user.confirmation_code = send_mail_code(request.data)
    user.save()
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def get_token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data['username']
    # user = get_object_or_404(User, username=username)
    confirmation_code = serializer.validated_data['confirmation_code']

    user_token = get_object_or_404(User, username=username)
    if confirmation_code == user_token.confirmation_code:
        token = str(AccessToken.for_user(user_token))
        return Response({'token((JWT-токен))': token},
                        status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminOrReadOnly, )
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('username', )
    lookup_field = 'username'

    @action(methods=['GET', 'PATCH'],
            detail=False,
            permission_classes=[permissions.IsAuthenticated]
            )
    def get_patch_me(self, request):
        user = get_object_or_404(User, username=self.request.user)
        if request.method == 'GET':
            serializer = UserMeSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == 'PATCH':
            serializer = UserMeSerializer(
                user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)


class ReviewsViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination

    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsAuthor)
    # permission_classes = (MyPermission,) 

    def get_queryset(self):
        new_queryset = Review.objects.filter(title=self.kwargs.get("title_id"))
        return new_queryset

    def perform_create(self, serializer):
        user = User.objects.get(username=self.request.user)
        if Review.objects.filter(title=self.kwargs.get("title_id"), author=user.id).exists():
            raise ValidationError("entry is already exist.")
        serializer.save(
            title=get_object_or_404(Title, id=self.kwargs.get("title_id")),
            author=get_object_or_404(User, username=self.request.user),
        )

    def perform_update(self, serializer):
        serializer.save(
            title=get_object_or_404(Title, id=self.kwargs.get("title_id")),
            author=get_object_or_404(User, username=self.request.user),
        )


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer

    pagination_class = PageNumberPagination
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsAuthor)

    def get_queryset(self):
        # print(self.kwargs.get("review_id"))
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
    """
    Получить список всех жанров.
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    #permission_classes = (IsAdminUserOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name', )
    lookup_field = 'slug'


class CategoryViewSet(viewsets.ModelViewSet):
    """
    Получить список всех категорий.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsAuthor)
    #permission_classes = (IsAdminUserOrReadOnly,)
    filter_backends = (SearchFilter, )
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    """
    Получить список всех объектов.
    """
    #queryset = Title.objects.annotate(rating=Avg("reviews__score"))
    queryset = Title.objects.all()
    #permission_classes = (IsAdminUserOrReadOnly, )
    # filter_backends = (DjangoFilterBackend, OrderingFilter)
    ordering_fields = ("name",)

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return TitleReadSerializer
        return TitleWriteSerializer
