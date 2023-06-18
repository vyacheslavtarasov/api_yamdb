from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from reviews.validators import UsernameValidatorRegex, username_me


class User(AbstractUser):
    """Модель переопределенного юзера."""

    ROLE_CHOICES = [
        ("user", "user"),
        ("moderator", "moderator"),
        ("admin", "admin"),
    ]
    username = models.CharField(
        validators=(UsernameValidatorRegex(), username_me),
        max_length=150,
        unique=True,
    )
    first_name = models.CharField(max_length=150, null=True)
    last_name = models.CharField(max_length=150, null=True)
    email = models.EmailField(
        blank=True,
        max_length=254,
        unique=True,
        verbose_name="email address",
    )
    role = models.CharField(
        verbose_name="Пользовательская роль",
        choices=ROLE_CHOICES,
        default="user",
        max_length=50,
    )
    bio = models.TextField("Биография", null=True)
    confirmation_code = models.CharField(
        "Код подтверждения пользователя", max_length=100, null=True
    )

    REQUIRED_FIELDS = ["email"]
    USERNAME_FIELDS = "email"

    # def __str__(self):
    #     return str(self.username)

    @property
    def is_admin(self):
        return self.role == "admin" or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == "moderator"

    @property
    def is_user(self):
        return self.role == "user"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["-id"]

    def __str__(self):
        return str(self.username)


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

    review_id = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name="reviews"
    )
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="users"
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ["-id"]

    def __str__(self):
        return self.text
