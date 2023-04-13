from django.db import models


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


class Title(models.Model):
    name = models.CharField(
        max_length=256,
        unique=True,
        db_index=True,
        verbose_name='Название произведения'
    )
    year = models.IntegerField()
    description = models.TextField()
    genre = models.ManyToManyField(
        through='GenreTitle',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='titles',
        verbose_name='Жанр'
    )
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='titles'
    )


class GenreTitle(models.Model):
    genre = models.ForeignKey(
        Genre,
        related_name='genre_title',
        on_delete=models.CASCADE,
    )
    title = models.ForeignKey(
        Title,
        related_name='genre_title',
        on_delete=models.CASCADE,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['genre', 'title'],
                name='unique_genre_title'
            ),
        ]


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
