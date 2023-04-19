from django.conf import settings
from django.db import models

from django.core.validators import MaxValueValidator, MinValueValidator

from users.models import User


class Genre(models.Model):
    name = models.CharField(
        max_length=256,
        unique=True,
        verbose_name='Жанр'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Слаг жанра'
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('name', )

    def __str__(self):
        return self.name[:settings.DISP_LETTERS]


class Title(models.Model):
    name = models.CharField(
        max_length=256,
        db_index=True,
        verbose_name='Название произведения'
    )
    year = models.IntegerField()
    description = models.TextField(
        blank=True,
        null=True,
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        through_fields=('title_id', 'genre_id'),
        related_name='titles',
        verbose_name='Жанр'
    )
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,

        blank=True,
        null=True,
        related_name='titles',
        verbose_name='Категория'
    )

    class Meta:
        ordering = ('name', )
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        constraints = [models.UniqueConstraint(
            fields=('name', 'category'),
            name='name_category'
        )]

    def __str__(self):
        return self.name[:settings.DISP_LETTERS]


class GenreTitle(models.Model):
    genre_id = models.ForeignKey(
        Genre,
        related_name='genre_title',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    title_id = models.ForeignKey(
        Title,
        related_name='genre_title',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['genre_id', 'title_id'],
                name='unique_genre_title'
            ),
        ]

    def __str__(self):
        return f'{self.title.id} - {self.genre.id}'


class Category(models.Model):
    name = models.CharField(
        max_length=256,
        unique=True,
        verbose_name='Категория'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Слаг категории'
    )

    class Meta:
        ordering = ('name', )
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name[:settings.DISP_LETTERS]


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Заголовок'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата отзыва'
    )
    text = models.TextField()
    score = models.PositiveSmallIntegerField(
        default=0,
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)],
        verbose_name='Оценка'
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-pub_date',)
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'], name="unique_review_id")
        ]


class Comment(models.Model):
    review_id = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата комментария'
    )
    text = models.TextField()

    class Meta:
        verbose_name = 'Коментарий'
        verbose_name_plural = 'Коментарии'

    def __str__(self):
        return self.author
