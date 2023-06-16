from django.contrib import admin

from .models import Category, Genre, Title, Review, Comments, User


class CommentsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Comments._meta.get_fields()]


class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "username",
        "bio",
        "role"
    )


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
    )


class GenreAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Genre._meta.get_fields()]


class TitleAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "year",
        "category",
        "description"
    )


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "text",
        "author",
        "score",
        "pub_date"
    )


admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comments, CommentsAdmin)
admin.site.register(User, UserAdmin)
