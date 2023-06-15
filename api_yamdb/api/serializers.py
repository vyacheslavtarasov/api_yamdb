from django.core.exceptions import ValidationError
from rest_framework.validators import UniqueValidator
from rest_framework import serializers
# from django.http import HTTP 

from reviews.models import (
    Review,
    Comments,
    Genre,
    User,
    Category,

)


class SignUpSerializer(serializers.ModelSerializer):
    """Сериализатор формы регистрации.POST-запрос: username и email."""
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        required=True,
        # validators=[UsernameRegexValidator(), ]
    )

    def username_me(value):
        """Проверка имени пользователя (me недопустимое имя)."""
        if value == 'me':
            raise ValidationError(
                'Имя пользователя "me" не разрешено.'
            )
        return value

    class Meta:
        model = User
        fields = ('username', 'email')


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
