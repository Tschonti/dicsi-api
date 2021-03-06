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
    songs = SongInPlaylistSerializer(source='songinplaylist_set', many=True, allow_empty=True, required=False)

    class Meta:
        model = Playlist
        fields = ['id', 'name', 'songs', 'created_at']

    def create(self, validated_data):
        songs_data = ''
        if 'songinplaylist_set' in validated_data:
            songs_data = validated_data.pop('songinplaylist_set')
        playlist = Playlist.objects.create(**validated_data)
        if songs_data:
            for songInPlaylist_data in songs_data:
                SongInPlaylist.objects.create(playlist=playlist, **songInPlaylist_data)
        return playlist

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        if 'songinplaylist_set' in validated_data:
            songs_data = validated_data.pop('songinplaylist_set')
            songInPlaylistIds = []
            for songInPlaylist_data in songs_data:
                SongInPlaylist.objects.update_or_create(defaults=songInPlaylist_data, playlist=instance, song=songInPlaylist_data['song'])
                songInPlaylistIds.append(songInPlaylist_data['song'].id)
            for songInPlaylistToBeRemoved in instance.songs.all():
                if songInPlaylistToBeRemoved.id not in songInPlaylistIds:
                    instance.songs.remove(songInPlaylistToBeRemoved)
        return instance