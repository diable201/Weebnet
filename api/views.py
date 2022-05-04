import logging
from django.http import JsonResponse
from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from api.models import Genre, Anime, Manga, LightNovel, Comment
from api.serializers import (
    GenreBaseSerializer, AnimeBaseSerializer,
    AnimeListResponseSerializer, AnimeRetrieveResponseSerializer,
    MangaBaseSerializer, MangaDetailSerializer,
    LightNovelBaseSerializer, LightNovelDetailSerializer,
    CommentRequestSerializer, CommentListSerializer
)
logger = logging.getLogger(__name__)


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


class GenreSearchView(APIView):
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


class AnimeSearchView(APIView):
    permission_classes = (IsAuthenticated,)
    queryset = Anime.objects.all()
    serializer_class = AnimeBaseSerializer

    @action(methods=["GET"], detail=False)
    def get(self, request):
        logger.info("LOG MESSAGE")
        search = self.request.query_params.get('search', None)
        if search:
            queryset = self.queryset.filter(title__icontains=search)
            serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response([], status=status.HTTP_200_OK)


class MangaViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin
):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Manga.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve' or self.action == 'update':
            return MangaDetailSerializer
        return MangaBaseSerializer


class MangaSearchView(APIView):
    permission_classes = (IsAuthenticated,)
    queryset = Manga.objects.all()
    serializer_class = MangaBaseSerializer

    @action(methods=["GET"], detail=False)
    def get(self, request):
        logger.info("LOG MESSAGE")
        search = self.request.query_params.get('search', None)
        if search:
            queryset = self.queryset.filter(title__icontains=search)
            serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response([], status=status.HTTP_200_OK)


class LightNovelViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin
):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return LightNovel.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve' or self.action == 'update':
            return LightNovelDetailSerializer
        return LightNovelBaseSerializer


class LightNovelSearchView(APIView):
    permission_classes = (IsAuthenticated,)
    queryset = LightNovel.objects.all()
    serializer_class = LightNovelBaseSerializer

    @action(methods=["GET"], detail=False)
    def get(self, request):
        logger.info("LOG MESSAGE")
        search = self.request.query_params.get('search', None)
        if search:
            queryset = self.queryset.filter(title__icontains=search)
            serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response([], status=status.HTTP_200_OK)


class CommentViewSet(viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == 'create_comment':
            return CommentRequestSerializer
        elif self.action == 'get_comments':
            return CommentListSerializer
        return None

    def get_queryset(self):
        return Comment.objects.filter(anime=self.kwargs.get('pk'))

    @action(methods=('post',), detail=False)
    def create_comment(self, request, *args, **kwargs):
        logger.info("LOG MESSAGE")
        serializer = self.get_serializer(data=self.request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=('get',), detail=False)
    def get_comments(self, request, *args, **kwargs):
        logger.info("LOG MESSAGE")
        comments = self.get_queryset()
        serializer = self.get_serializer(comments, many=True)
        return Response(serializer.data)


def anime_top_ten(request):
    logger.info("LOG MESSAGE")
    anime = Anime.objects.all().order_by('-score')[:10]
    anime_json = [_.to_json() for _ in anime]
    return JsonResponse(anime_json, safe=False)


def manga_top_ten(request):
    logger.info("LOG MESSAGE")
    manga = Manga.objects.all().order_by('-score')[:10]
    manga_json = [_.to_json() for _ in manga]
    return JsonResponse(manga_json, safe=False)


def get_nsfw_anime(request):
    logger.info("OH NO CRINGE")
    anime = Anime.adult_objects.all()
    anime_json = [_.to_json() for _ in anime]
    return JsonResponse(anime_json, safe=False)
