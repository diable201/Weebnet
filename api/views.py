from rest_framework import generics, mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import (
    GenreBaseSerializer, AnimeBaseSerializer,
    AnimeListResponseSerializer, AnimeRetrieveResponseSerializer
)
from api.models import Genre, Anime


class GenreViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin
):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Genre.objects.all()

    def get_serializer_class(self):
        return GenreBaseSerializer


class GenreSearchView(
    APIView
):
    permission_classes = (IsAuthenticated,)
    queryset = Genre.objects.all()
    serializer_class = GenreBaseSerializer

    @action(methods=["GET"], detail=False)
    def get(self, request):
        search = self.request.query_params.get('search', None)
        if search:
            queryset = self.queryset.filter(name__icontains=search)
            serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response([], status=status.HTTP_200_OK)


class AnimeViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin
):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Anime.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return AnimeListResponseSerializer
        if self.action == 'retrieve':
            return AnimeRetrieveResponseSerializer
        return AnimeBaseSerializer
