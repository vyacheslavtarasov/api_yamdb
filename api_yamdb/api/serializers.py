# from django.core.exceptions import ValidationError
from rest_framework.validators import UniqueValidator
from rest_framework import serializers
# from django.http import HTTP

from reviews.models import (
    Review,
    Comments,
    Genre,
    User,
    Category,
    username_me,
    Titles,
)
from reviews.validators import UsernameValidatorRegex, username_me


class SignUpSerializer(serializers.ModelSerializer):
    """Сериализатор формы регистрации.POST-запрос: username и email."""
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        required=True,
        validators=[UsernameValidatorRegex(), ]
    )

    def validate_username(self, value):
        """Проверка имени пользователя (me недопустимое имя)."""
        return username_me(value)

    class Meta:
        model = User
        fields = ('username', 'email')


class TokenSerializer(serializers.ModelSerializer):
    """Сериализатор получения JWT-токена."""
    username = serializers.CharField(
        required=True,
        validators=(UsernameValidatorRegex(), )
    )
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')

    def validate_username(self, value):
        return username_me(value)


class ReviewSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(
        read_only=True, slug_field="username"
    )

    title_id = serializers.SlugRelatedField(
        read_only=True, slug_field="id"
    )

    class Meta:
        fields = "__all__"
        model = Review


class CommentsSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(
        read_only=True, slug_field="username"
    )

    review_id = serializers.SlugRelatedField(
        read_only=True, slug_field="id"
    )

    class Meta:
        fields = "__all__"
        model = Comments


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Genre


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Category


class TitlesReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(
        read_only=True,
        many=True
    )
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Titles


class TitlesWriteSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )

    class Meta:
        fields = '__all__'
        model = Titles
