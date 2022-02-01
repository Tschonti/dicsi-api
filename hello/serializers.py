from dataclasses import fields
from rest_framework import serializers
import json

from .models import Song, Playlist, SongInPlaylist


class SongInPlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = SongInPlaylist
        fields = ['song', 'place']

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

class PlaylistSerializer(serializers.ModelSerializer):
    #songs = serializers.PrimaryKeyRelatedField(queryset=Song.objects.all(), many=True, allow_empty=True, required=False)
    songs = SongInPlaylistSerializer(source='songinplaylist_set', many=True, allow_empty=True, required=False)

    class Meta:
        model = Playlist
        fields = ['id', 'name', 'songs', 'created_at']

    def create(self, validated_data):
        playlist = Playlist.objects.create(**validated_data)
        songs_data = validated_data.pop('songinplaylist_set')
        for songInPlaylist_data in songs_data:
            SongInPlaylist.objects.create(playlist=playlist, **songInPlaylist_data)
        return playlist