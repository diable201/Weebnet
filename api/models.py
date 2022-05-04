from django.db import models

import sso.models
from api.managers import NSFWManager
from api.utils import validate_size, validate_extension


class TimestampMixin(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Время создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Время последнего изменения'
    )


class Genre(TimestampMixin):
    name = models.CharField(
        max_length=200,
        verbose_name='Название'
    )
    icon = models.ImageField(
        upload_to='images/genre/',
        null=True,
        blank=True,
        verbose_name='Иконка'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание'
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return f'{self.id}: {self.name}'


class Anime(TimestampMixin):
    ONGOING = 'ONGOING'
    RELEASED = 'RELEASED'

    MANGA = 'MANGA'
    LIGHT_NOVEL = 'LIGHT_NOVEL'

    ANIME_STATUS_CHOICES = (
        (ONGOING, 'Онгоинг'),
        (RELEASED, 'Выпущено'),
    )

    SOURCE_CHOICES = (
        (MANGA, 'Манга'),
        (LIGHT_NOVEL, 'Лайт новелла')
    )

    title = models.CharField(
        max_length=200,
        verbose_name='Название'
    )
    source = models.CharField(
        choices=SOURCE_CHOICES,
        null=True,
        blank=True,
        max_length=255,
        verbose_name='Источник'
    )
    episodes = models.IntegerField(
        default=0,
        verbose_name='Количество эпизодов'
    )
    score = models.FloatField(
        default=0.0,
        verbose_name='Рейтинг'
    )
    status = models.CharField(
        choices=ANIME_STATUS_CHOICES,
        blank=True,
        max_length=255,
        verbose_name='Статус'
    )
    synopsis = models.TextField(
        blank=True,
        verbose_name='Синопсис'
    )
    is_adult = models.BooleanField(
        default=False,
        verbose_name='NSFW?'
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        null=True,
        related_name='anime',
        verbose_name='Жанр'
    )

    objects = models.Manager()
    adult_objects = NSFWManager()

    class Meta:
        verbose_name = 'Аниме'
        verbose_name_plural = 'Аниме'

    def to_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'source': self.source,
            'episodes': self.episodes,
            'score': self.score,
            'status': self.status,
            'synopsis': self.synopsis,
            'genre': self.genre.name
        }

    def __str__(self):
        return f'{self.id}: {self.title} | {self.score}'


class Manga(TimestampMixin):
    ONGOING = 'ONGOING'
    RELEASED = 'RELEASED'

    MANGA_STATUS_CHOICES = (
        (ONGOING, 'Онгоинг'),
        (RELEASED, 'Выпущено'),
    )

    title = models.CharField(
        max_length=200,
        verbose_name='Название'
    )
    volumes = models.IntegerField(
        default=0,
        verbose_name='Количество томов'
    )
    chapters = models.IntegerField(
        default=0,
        verbose_name='Количество глав'
    )
    score = models.FloatField(
        default=0.0,
        verbose_name='Рейтинг'
    )
    status = models.CharField(
        choices=MANGA_STATUS_CHOICES,
        blank=True,
        max_length=255,
        verbose_name='Статус'
    )
    synopsis = models.TextField(
        blank=True,
        verbose_name='Синопсис'
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        null=True,
        related_name='manga',
        verbose_name='Жанр'
    )

    class Meta:
        verbose_name = 'Манга'
        verbose_name_plural = 'Манга'

    def to_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'volumes': self.volumes,
            'chapters': self.chapters,
            'score': self.score,
            'status': self.status,
            'synopsis': self.synopsis,
            'genre': self.genre.name
        }

    def __str__(self):
        return f'{self.id}: {self.title} | {self.score}'


class LightNovel(TimestampMixin):
    ONGOING = 'ONGOING'
    RELEASED = 'RELEASED'

    LIGHT_NOVEL_STATUS_CHOICES = (
        (ONGOING, 'Онгоинг'),
        (RELEASED, 'Выпущено'),
    )

    title = models.CharField(
        max_length=200,
        verbose_name='Название'
    )
    volumes = models.IntegerField(
        default=0,
        verbose_name='Количество томов'
    )
    chapters = models.IntegerField(
        default=0,
        verbose_name='Количество глав'
    )
    score = models.FloatField(
        default=0.0,
        verbose_name='Рейтинг'
    )
    status = models.CharField(
        choices=LIGHT_NOVEL_STATUS_CHOICES,
        blank=True,
        max_length=255,
        verbose_name='Статус'
    )
    synopsis = models.TextField(
        blank=True,
        verbose_name='Синопсис'
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        null=True,
        related_name='light_novel',
        verbose_name='Жанр'
    )

    class Meta:
        verbose_name = 'Ранобэ'
        verbose_name_plural = 'Ранобэ'

    def __str__(self):
        return f'{self.id}: {self.title} | {self.score}'


class Image(TimestampMixin):
    anime = models.ForeignKey(
        Anime,
        on_delete=models.DO_NOTHING,
        null=True,
        related_name='anime_images',
        verbose_name='Аниме'
    )
    manga = models.ForeignKey(
        Manga,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        related_name='manga_images',
        verbose_name='Манга'
    )
    light_novel = models.ForeignKey(
        LightNovel,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        related_name='light_novel_images',
        verbose_name='Ранобэ'
    )
    image = models.ImageField(
        upload_to='images/',
        validators=[validate_size, validate_extension],
        null=True,
        blank=True,
        verbose_name='Изображение'
    )

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'

    def __str__(self):
        return f'{self.id}'


class Comment(TimestampMixin):
    anime = models.ForeignKey(
        Anime,
        on_delete=models.CASCADE,
        verbose_name='Аниме'
    )

    user = models.ForeignKey(
        sso.models.User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )

    content = models.CharField(
        max_length=255,
        verbose_name='Текст'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f"{self.user}, {self.anime}, {self.content}"

