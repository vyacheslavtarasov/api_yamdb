from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Category, Comments, Genre, Review, Title


class CategoryResource(resources.ModelResource):
    # list = (field.name for field in Comments._meta.get_fields())
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
    list = (field.name for field in Comments._meta.get_fields())


class GenreAdmin(ImportExportModelAdmin):
    resource_classes = GenreResource
    list = (field.name for field in Comments._meta.get_fields())


class CommentsResource(resources.ModelResource):
    list = (field.name for field in Comments._meta.get_fields())


class CommentsAdmin(ImportExportModelAdmin):
    resource_classes = CommentsResource
    list = (field.name for field in Comments._meta.get_fields())


class TitleResource(resources.ModelResource):
    list = (field.name for field in Comments._meta.get_fields())


class TitleAdmin(ImportExportModelAdmin):
    resource_classes = TitleResource
    list = (field.name for field in Comments._meta.get_fields())


class ReviewResource(resources.ModelResource):
    list = (field.name for field in Comments._meta.get_fields())


class ReviewAdmin(ImportExportModelAdmin):
    resource_classes = ReviewResource
    list = (field.name for field in Comments._meta.get_fields())


admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comments, CommentsAdmin)
# admin.site.register(User, UserAdmin)
