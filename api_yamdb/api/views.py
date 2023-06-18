from django.db import IntegrityError
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from authorization.send_confirmation_code import send_mail_code
from api.filters import TitleFilter
from api.permissions import IsAdminOrReadOnly, IsAdmitOrGetOut, IsAuthor
from api.serializers import (
    CategorySerializer,
    CommentsSerializer,
    GenreSerializer,
    ReviewSerializer,
    SignUpSerializer,
    TitleReadSerializer,
    TitleWriteSerializer,
    TokenSerializer,
    UserMeSerializer,
    UserSerializer,
)
from reviews.models import Category, Comments, Genre, Review, Title, User
from user.models import User


@api_view(["POST"])
def signup_cust(request):
    """Регистрация пользователя."""

    if User.objects.filter(email=request.POST.get("email")).exists():
        if not User.objects.filter(
            username=request.POST.get("username")
        ).exists():
            return Response(
                "Такой логин или @email уже заняты! Ввведите другой.",
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response("ok", status=status.HTTP_200_OK)

    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    try:
        user, _ = User.objects.get_or_create(
            username=serializer.validated_data.get("username"),
            email=serializer.validated_data.get("email"),
        )
    except IntegrityError:
        return Response(
            "Такой логин или @email уже заняты! Ввведите другой.",
            status=status.HTTP_400_BAD_REQUEST,
        )

    user.confirmation_code = send_mail_code(request.data)
    user.save()
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def get_token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data["username"]

    confirmation_code = serializer.validated_data["confirmation_code"]

    user_token = get_object_or_404(User, username=username)
    if confirmation_code == user_token.confirmation_code:
        token = str(AccessToken.for_user(user_token))
        return Response(
            {"token((JWT-токен))": token}, status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ["get", "post", "patch", "delete"]
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ("=username",)
    lookup_field = "username"

    def perform_create(self, serializer):
        if self.request.user.role == "admin":
            if not self.request.POST.get("email"):
                raise ValidationError("entry is already exist.")
        serializer.save()

    def get_permissions(self):
        if self.action in ["list", "retrieve", "create"]:
            return (IsAdmitOrGetOut(),)
        return super().get_permissions()

    @action(
        methods=["GET", "PATCH"],
        detail=False,
        url_path="me",
        permission_classes=[permissions.IsAuthenticated],
    )
    def get_patch_me(self, request):
        user = get_object_or_404(User, username=self.request.user)
        if request.method == "GET":
            serializer = UserMeSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == "PATCH":
            serializer = UserMeSerializer(
                user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)


class ReviewsViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination

    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsAuthor)

    def get_queryset(self):
        return Review.objects.filter(title=self.kwargs.get("title_id"))

    def perform_create(self, serializer):
        serializer.save(
            title=get_object_or_404(Title, id=self.kwargs.get("title_id")),
            author=get_object_or_404(User, username=self.request.user),
        )

    def perform_update(self, serializer):
        serializer.save(
            title=get_object_or_404(Title, id=self.kwargs.get("title_id")),
        )


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer

    pagination_class = PageNumberPagination
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsAuthor)

    def get_queryset(self):
        new_queryset = Comments.objects.filter(
            review=self.kwargs.get("review_id")
        )
        return new_queryset

    def perform_create(self, serializer):
        serializer.save(
            review=get_object_or_404(
                Review, id=self.kwargs.get("review_id")
            ),
            author=get_object_or_404(User, username=self.request.user),
        )

    def perform_update(self, serializer):
        serializer.save(
            review=get_object_or_404(
                Review, id=self.kwargs.get("review_id")
            ),
            author=get_object_or_404(User, username=self.request.user),
        )


class GenreViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """
    Получить список всех жанров.
    """

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"


class CategoryViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """
    Получить список всех категорий.
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    lookup_field = "slug"
    search_fields = ("name",)


class TitleViewSet(viewsets.ModelViewSet):
    """
    Получить список всех объектов.
    """
    queryset = Title.objects.annotate(
        rating=Avg("reviews__score")).order_by("id")
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    ordering_fields = ("name",)

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return TitleReadSerializer
        return TitleWriteSerializer
