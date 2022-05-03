from django.urls import path
from rest_framework.routers import DefaultRouter

from api.views import GenreViewSet, GenreSearchView, AnimeViewSet

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
        name="get/create items",
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
]

urlpatterns += router.urls
