from django.contrib import admin

from .models import Category, Comments, Genre, Review, Title, User


class CommentsAdmin(admin.ModelAdmin):
    list_display = ("text", "author", "pub_date", "review_id")


class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "bio", "role")


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
    )


class GenreAdmin(admin.ModelAdmin):
    list_display = ("slug", "name")


class TitleAdmin(admin.ModelAdmin):
    list_display = ("name", "year", "category", "description")


class ReviewAdmin(admin.ModelAdmin):
    list_display = ("title", "text", "author", "score", "pub_date")


admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comments, CommentsAdmin)
admin.site.register(User, UserAdmin)
