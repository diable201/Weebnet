from django.contrib import admin
from .models import Anime, Genre


@admin.register(Anime)
class AnimeAdmin(admin.ModelAdmin):
    ordering = ('id', )
    list_display = (
        'id',
        'title',
        'source',
        'score',
        'status'
    )
    list_editable = ('status',)
    list_filter = ('status', 'genre')


@admin.register(Genre)
class GenreAnime(admin.ModelAdmin):
    class AnimeInline(admin.TabularInline):
        model = Anime
        extra = 1
    ordering = ('id',)
    list_display = (
        'id',
        'name',
        'description'
    )
    inlines = (AnimeInline,)

