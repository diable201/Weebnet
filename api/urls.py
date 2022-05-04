from django.urls import path
from rest_framework.routers import DefaultRouter

from api.views import GenreViewSet, GenreSearchView, AnimeViewSet, MangaViewSet, LightNovelViewSet

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
]

urlpatterns += router.urls
