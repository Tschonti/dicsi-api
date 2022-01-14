from rest_framework import serializers

from .models import Song, Playlist

class SongSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=256)
    lyrics = serializers.CharField(max_length=5000)
    verses = serializers.ListField(
        child=serializers.CharField(max_length=5000), allow_empty=True, required=False
    )

    def create(self, validated_data):
        return Song.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.lyrics = validated_data.get('lyrics', instance.lyrics)

        instance.save()
        return instance

    def to_representation(self, instance):
        ret =  super().to_representation(instance)
        ret['verses'] = ret['lyrics'].split('###')
        return ret

class PlaylistSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=256)
    created_at = serializers.DateTimeField()
    songs = serializers.PrimaryKeyRelatedField(queryset=Song.objects.all(), many=True)

    def create(self, validated_data):
        return Playlist.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.created_at = validated_data.get('created_at', instance.created_at)
        instance.songs = validated_data.get('songs', instance.songs)

        instance.save()
        return instance