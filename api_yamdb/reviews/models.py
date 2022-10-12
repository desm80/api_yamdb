from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import User
from .validators import validate_year


class Category(models.Model):
    """Модель категории произведения."""

    name = models.CharField(
        verbose_name="Название категории",
        unique=True,
        max_length=256,
    )

    slug = models.SlugField(
        verbose_name="Адрес категории",
        unique=True,
        max_length=50,
    )

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"
        ordering = ("id",)

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель жанров произведений."""

    name = models.CharField(verbose_name="Жанр", max_length=256)

    slug = models.SlugField(
        verbose_name="Адрес жанра",
        unique=True,
        max_length=50,
    )

    class Meta:
        verbose_name = "жанр"
        verbose_name_plural = "жанры"
        ordering = ("id",)

    def __str__(self):
        return self.name



class Title(models.Model):
    """Модель произведения."""

    name = models.CharField(
        verbose_name="Название произведения", 
        max_length=256,
        blank=False,
    )

    year = models.PositiveSmallIntegerField(
        verbose_name="Год создания произведения",
        blank=True,
        validators=[validate_year],
    )

    description = models.CharField(
        verbose_name="Описание произведения",
        max_length=256,
        blank=True,
    )

    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        related_name="genre",
        verbose_name="Жанр произведения",
        blank=True,
    )
    category = models.ForeignKey(
        Category,
        verbose_name="Описание категории",
        related_name="category",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"
        ordering = ("id",)

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.genre} {self.title}'


class Review(models.Model):
    """Модель отзывов."""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    text = models.TextField()

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    score = models.IntegerField(
        'Оценка',
        default=0,
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ],
    )
    pub_date = models.DateTimeField(
        "Дата добавления", 
        auto_now_add=True, 
        db_index=True
    )

    class Meta:
        odering = ["-pub_date"]
        verbose_name = "отзыв"
        verbose_name_plural = "отзывы"
        constraints = [
            models.UniqueConstraint(
                fields=("author", "title"), name="unique_review"
            )
        ]


class Comment(models.Model):
    """Модель комментариев."""

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    pub_date = models.DateTimeField(
        "Дата добавления",
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = "коментарий"
        verbose_name_plural = "комментариев"

    def __str__(self):
        return self.text