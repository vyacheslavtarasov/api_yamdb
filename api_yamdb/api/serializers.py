from rest_framework import serializers

from reviews.models import (
    Review, 
    Comments,
    Genre,
    Category,
)


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
