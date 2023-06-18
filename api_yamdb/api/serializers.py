from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator

from reviews.models import Category, Comments, Genre, Review, Title, User
from reviews.validators import UsernameValidatorRegex, username_me


class SignUpSerializer(serializers.ModelSerializer):
    """Сериализатор формы регистрации.POST-запрос: username и email."""

    email = serializers.EmailField(
        max_length=150,
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    username = serializers.CharField(
        max_length=150,
        required=True,
        validators=[
            UsernameValidatorRegex(),
        ],
    )

    def validate(self, data):
        if data["username"] == "me":
            raise serializers.ValidationError("Нельзя использовать логин me")
        return data

    class Meta:
        model = User
        fields = ("username", "email")


class TokenSerializer(serializers.ModelSerializer):
    """Сериализатор получения JWT-токена."""

    username = serializers.CharField(
        max_length=150, required=True, validators=(UsernameValidatorRegex(),)
    )
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ("username", "confirmation_code")

    def validate_username(self, value):
        return username_me(value)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )


class UserMeSerializer(serializers.ModelSerializer):
    role = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )
        read_only_fields = ("role",)


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field="username"
    )

    title = serializers.SlugRelatedField(read_only=True, slug_field="id")

    class Meta:
        fields = "__all__"
        model = Review

    def validate(self, data):
        user = self.context["request"].user
        title_id = self.context["view"].kwargs.get("title_id")
        if (
            Review.objects.filter(title=title_id, author=user).exists()
            and self.context["request"].method == "POST"
        ):
            raise ValidationError("Entry is already exist.")
        return data


class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field="username"
    )

    review_id = serializers.SlugRelatedField(read_only=True, slug_field="id")

    class Meta:
        fields = "__all__"
        model = Comments


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ("name", "slug")


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("name", "slug")


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = "__all__"
        model = Title


class TitleWriteSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field="slug"
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), slug_field="slug", many=True
    )

    class Meta:
        fields = "__all__"
        model = Title
