from django.contrib import admin

from .models import Category, Genre, Titles
# Review, Comments


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
    )


class GenreAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
    )


class TitlesAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "year",
        "category",
    )


admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Titles, TitlesAdmin)
# admin.site.register(Genre, GenreAdmin)
