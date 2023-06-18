
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from user.models import User


class Category(models.Model):
    """Модель Категорий. Типы произведений.
    Одно произведение может быть привязано только к одной категории"""

    name = models.CharField(verbose_name="Название категории", max_length=200)
    slug = models.SlugField(
        verbose_name="Slug названия категории",
        unique=True
        # Так как у нас будет csv здесь будет index БД
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["-id"]

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель жанров.
    Одно произведение может быть привязано к нескольким жанрам."""

    name = models.CharField(verbose_name="Название жанра", max_length=200)
    slug = models.SlugField(
        verbose_name="Slug названия жанра",
        unique=True
        # Так как у нас будет csv здесь будет index БД
    )

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"
        ordering = ["-id"]

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель произведений. Произведения, к которым пишут
    отзывы (определённый фильм, книга или песенка)."""

    name = models.CharField(
        verbose_name="Название произведения",
        max_length=200,
        # Так как у нас будет csv здесь будет index БД
    )
    year = models.IntegerField()
    description = models.TextField()
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name="categories",
        blank=True,
        null=True,
    )
    genre = models.ManyToManyField(
        Genre, related_name="title", verbose_name="Жанр"
    )

    class Meta:
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Review(models.Model):
    """Отзывы на произведения.
    Отзыв привязан к определённому произведению."""

    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name="reviews"
    )
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reviews"
    )
    score = models.PositiveSmallIntegerField(
        validators=(MaxValueValidator(10), MinValueValidator(1))
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Ревью"
        verbose_name_plural = "Ревью"
        unique_together = (("title", "author"),)
        ordering = ["-id"]

    def __str__(self):
        return self.text[:30]


class Comments(models.Model):
    """Комментарии к отзывам.
    Комментарий привязан к определённому отзыву."""

    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name="reviews"
    )
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user"
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ["-id"]

    def __str__(self):
        return self.text
