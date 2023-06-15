# from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from reviews.validators import UsernameValidatorRegex, username_me


class User(AbstractUser):
    """Модель переопределенного юзера."""
    ROLE_CHOICES = [
        ('user', 'user'),
        ('moderator', 'moderator'),
        ('admin', 'admin'),
    ]
    username = models.CharField(
        'Имя пользователя',
        validators=(UsernameValidatorRegex(), username_me),
        max_length=150,
        unique=True,
        # validators=[username_validator],
    )
    first_name = models.CharField(max_length=150, null=True)
    last_name = models.CharField(max_length=150, null=True)
    email = models.EmailField(
        blank=True,
        max_length=254,
        unique=True,
        verbose_name='email address',
    )
    role = models.CharField(
        verbose_name='Пользовательская роль',
        choices=ROLE_CHOICES,
        default='user',
        max_length=50)
    bio = models.TextField('Биография', null=True)
    confirmation_code = models.CharField(
        'Код подтверждения пользователя',
        max_length=100,
        null=True
    )

    REQUIRED_FIELDS = ['email']
    USERNAME_FIELDS = 'email'

    def __str__(self):
        return str(self.username)

    @property
    def is_admin(self):
        return self.role == "admin" or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == "moderator"

    @property
    def is_user(self):
        return self.role == "user"


class Category(models.Model):
    """Модель Категорий. Типы произведений.
    Одно произведение может быть привязано только к одной категории"""
    name = models.CharField(
        verbose_name='Название категории',
        max_length=200
    )
    slug = models.SlugField(
        verbose_name='Slug названия категории',
        unique=True
        # Так как у нас будет csv здесь будет index БД
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель жанров.
    Одно произведение может быть привязано к нескольким жанрам."""
    name = models.CharField(
        verbose_name='Название жанра',
        max_length=200
    )
    slug = models.SlugField(
        verbose_name='Slug названия жанра',
        unique=True
        # Так как у нас будет csv здесь будет index БД
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Titles(models.Model):
    """Модель произведений. Произведения, к которым пишут
    отзывы (определённый фильм, книга или песенка)."""
    name = models.CharField(
        verbose_name='Название произведения',
        max_length=200,
        # Так как у нас будет csv здесь будет index БД
    )
    year = models.DateTimeField('Дата произведения')
    description = models.TextField()
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='categories',
        blank=True,
        null=True,
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Жанр'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Review(models.Model):
    """Отзывы на произведения.
    Отзыв привязан к определённому произведению."""
    title_id = models.ForeignKey(
        Titles,
        on_delete=models.CASCADE,
        related_name="titles"
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user"
    )
    score = models.IntegerField()
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Ревью'
        verbose_name_plural = 'Ревью'

    def __str__(self):
        return self.text


class Comments(models.Model):
    """Комментарии к отзывам.
    Комментарий привязан к определённому отзыву."""
    review_id = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="users"
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text
