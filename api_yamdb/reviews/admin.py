from import_export import resources
from import_export.admin import ImportExportModelAdmin

from django.contrib import admin

from .models import Category, Comments, Genre, Review, Title


class CategoryResource(resources.ModelResource):
    """CategoryResource от ModelResource из django-import-export.
    Он определяет, какие данные должны быть экспортированы и
    импортированы в модель Category, и настраивает
    экспортированные/импортированные поля модели Category."""

    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "slug",
        )


class CategoryAdmin(ImportExportModelAdmin):
    """Он регистрирует модель Category для использования в
    административной панели Django и определяет,
    как отображать экспортированные данные для Category
    в административной панели Django.
    """

    resource_classes = (CategoryResource,)
    list_display = (
        "id",
        "name",
        "slug",
    )


class GenreResource(resources.ModelResource):
    class Meta:
        model = Genre
        fields = (
            "id",
            "name",
            "slug",
        )


class GenreAdmin(ImportExportModelAdmin):
    resource_classes = (GenreResource,)
    list_display = (
        "id",
        "name",
        "slug",
    )


class CommentsResource(resources.ModelResource):
    class Meta:
        model = Comments
        fields = ("id", "review", "text", "author", "pub_date")


class CommentsAdmin(ImportExportModelAdmin):
    resource_classes = (CommentsResource,)
    list_display = ("id", "review", "text", "author", "pub_date")


class TitleResource(resources.ModelResource):
    class Meta:
        model = Title
        fields = ("id", "name", "year", "description", "category", "genre")


class TitleAdmin(ImportExportModelAdmin):
    resource_classes = (TitleResource,)
    list_display = ("id", "name", "year", "description", "category")


class ReviewResource(resources.ModelResource):
    class Meta:
        model = Review
        fields = ("id", "title", "text", "author", "score", "pub_date")


class ReviewAdmin(ImportExportModelAdmin):
    resource_classes = ReviewResource
    list_display = ("id", "title", "text", "author", "score", "pub_date")


admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comments, CommentsAdmin)
