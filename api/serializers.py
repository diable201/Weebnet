from rest_framework import serializers

from api.models import Anime, Genre


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

    def create(self, validated_data):
        return Anime.objects.create(**validated_data)

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
    images = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    genre = serializers.StringRelatedField()


class AnimeListResponseSerializer(AnimeBaseSerializer):
    images = serializers.StringRelatedField(many=True, read_only=True)
    genre = serializers.StringRelatedField()
