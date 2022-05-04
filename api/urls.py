from django.urls import path
from rest_framework.routers import DefaultRouter

from api.views import (
    GenreViewSet, GenreSearchView, AnimeViewSet,
    MangaViewSet, LightNovelViewSet, CommentViewSet,
    AnimeSearchView, LightNovelSearchView, MangaSearchView,
    anime_top_ten, manga_top_ten, get_nsfw_anime
)

app_name = 'api'

router = DefaultRouter()

urlpatterns = [
    path(
        "genres/",
        GenreViewSet.as_view(
            {
                "get": "list",
                "post": "create",
            }),
        name="get/create genres",
    ),
    path(
        "genres/<int:pk>/",
        GenreViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                'delete': 'destroy'
            }),
        name="get/put genre",
    ),
    path(
        r'categories/search/',
        GenreSearchView.as_view()
    ),
    path(
        "anime/",
        AnimeViewSet.as_view(
            {
                "get": "list",
                "post": "create",
            }),
        name="get/create manga",
    ),
    path(
        "anime/<int:pk>/",
        AnimeViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                'delete': 'destroy'
            }),
        name="get/put anime",
    ),
    path(
        r'anime/search/',
        AnimeSearchView.as_view()
    ),
    path(
        'anime/top/',
        anime_top_ten
    ),
    path(
        'anime/nsfw/',
        get_nsfw_anime
    ),
    path(
        "manga/",
        MangaViewSet.as_view(
            {
                "get": "list",
                "post": "create",
            }),
        name="get/create manga",
    ),
    path(
        "manga/<int:pk>/",
        MangaViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                'delete': 'destroy'
            }),
        name="get/put manga",
    ),
    path(
        r'manga/search/',
        MangaSearchView.as_view()
    ),
    path(
        'manga/top/',
        manga_top_ten
    ),
    path(
        "light_novel/",
        LightNovelViewSet.as_view(
            {
                "get": "list",
                "post": "create",
            }),
        name="get/create light novel",
    ),
    path(
        "light_novel/<int:pk>/",
        LightNovelViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                'delete': 'destroy'
            }),
        name="get/put light novel",
    ),
    path(
        r'light_novel/search/',
        LightNovelSearchView.as_view()
    ),
    path(
        'comments/',
        CommentViewSet.as_view(
            {
                'post': 'create_comment'
            }),
        name='create comment'
    ),
    path(
        '<int:pk>/comments/',
        CommentViewSet.as_view(
            {
                'get': 'get_comments'
            }),
        name='get comments'
    ),
]

urlpatterns += router.urls
