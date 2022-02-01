from dataclasses import fields
from rest_framework import serializers
import json

from .models import Song, Playlist, SongInPlaylist

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

class SongInPlaylistSerializer(serializers.ModelSerializer):
    #song = serializers.PrimaryKeyRelatedField(queryset=Song.objects.all())
    #playlist = serializers.PrimaryKeyRelatedField(queryset=Playlist.objects.all())
    class Meta:
        model = SongInPlaylist
        fields = ['song', 'playlist', 'place']

class PlaylistSerializer(serializers.ModelSerializer):
    #songs = serializers.PrimaryKeyRelatedField(queryset=Song.objects.all(), many=True, allow_empty=True, required=False)
    songs = SongInPlaylistSerializer(many=True, read_only=True)

    class Meta:
        model = Playlist
        fields = ['id', 'name', 'songs', 'created_at']