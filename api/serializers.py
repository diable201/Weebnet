from rest_framework import serializers
from api.models import Anime, Genre, Manga, LightNovel, Image, Comment
from api.utils import validate_extension


class GenreBaseSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Genre
        fields = ['id', 'name', 'icon', 'description', 'created_at', 'updated_at']


class GenreSerializer(serializers.ModelSerializer):
    genre_id = serializers.IntegerField()

    class Meta:
        model = Genre
        fields = ('id',)


class ImageNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('image', 'anime', 'manga', 'light_novel')


class AnimeBaseSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    title = serializers.CharField()
    source = serializers.ChoiceField(choices=Anime.SOURCE_CHOICES)
    episodes = serializers.IntegerField()
    score = serializers.FloatField()
    status = serializers.ChoiceField(choices=Anime.ANIME_STATUS_CHOICES)
    synopsis = serializers.CharField()
    genre_id = serializers.IntegerField()
    anime_images = ImageNestedSerializer(many=True, read_only=True)

    def validate_genre_id(self, value):
        if value and not Genre.objects.filter(id=value).exists():
            raise serializers.ValidationError("Жанра не существует")
        return value

    def validate_episodes(self, value):
        if value and value < 0:
            raise serializers.ValidationError("Количество эпизодов должно быть больше нуля")
        return value

    def validate_score(self, value):
        if value and value < 0:
            raise serializers.ValidationError("Рейтинг должен быть больше положительным числом")
        return value

    def create(self, validated_data):
        anime_images = self.context.get('view').request.FILES
        anime = Anime.objects.create(**validated_data)
        for image in anime_images.values():
            try:
                validate_extension(image)
            except:
                raise serializers.ValidationError("Неподходящее разрешение")
            Image.objects.create(anime=anime, image=image)
        return anime


    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.source = validated_data.get('source', instance.source)
        instance.episodes = validated_data.get('episodes', instance.episodes)
        instance.score = validated_data.get('score', instance.score)
        instance.status = validated_data.get('status', instance.status)
        instance.synopsis = validated_data.get('synopsis', instance.synopsis)
        instance.genre_id = validated_data.get('genre_id', instance.genre_id)
        instance.save()
        return instance


class AnimeRetrieveResponseSerializer(AnimeBaseSerializer):
    anime_images = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    genre = serializers.StringRelatedField()


class AnimeListResponseSerializer(AnimeBaseSerializer):
    anime_images = serializers.StringRelatedField(many=True, read_only=True)
    genre = serializers.StringRelatedField()


class MangaBaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Manga
        fields = ('id', 'title', 'volumes', 'chapters', 'score', 'status')


class MangaDetailSerializer(MangaBaseSerializer):

    class Meta:
        model = Manga
        fields = ('id', 'title', 'volumes', 'score', 'status', 'synopsis', 'genre_id')


class LightNovelBaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = LightNovel
        fields = ('id', 'title', 'volumes', 'chapters', 'score', 'status')


class LightNovelDetailSerializer(LightNovelBaseSerializer):

    class Meta:
        model = LightNovel
        fields = ('id', 'title', 'volumes', 'score', 'status', 'synopsis', 'genre_id')


class CommentRequestSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Comment
        fields = ('anime', 'content', 'user')


class CommentListSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(
        source='user.first_name'
    )

    last_name = serializers.CharField(
        source='user.last_name'
    )

    email = serializers.CharField(
        source='user.email'
    )

    class Meta:
        model = Comment
        fields = ('id', 'first_name', 'last_name', 'email', 'content',)
