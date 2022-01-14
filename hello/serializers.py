from rest_framework import serializers
import json

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

#class PlaylistSerializer(serializers.Serializer):
#    id = serializers.IntegerField(allow_null=True, required=False)
#    name = serializers.CharField(max_length=256)
#    created_at = serializers.DateTimeField(allow_null=True, required=False)
#    songs = serializers.PrimaryKeyRelatedField(queryset=Song.objects.all(), many=True, allow_empty=True, required=False)
#
#    def create(self, validated_data):
#        pl = Playlist.objects.create(name=validated_data['name'])
#        pl.songs.set(validated_data.get('songs', []))
#        return pl
#
#    def update(self, instance, validated_data):
#        instance.name = validated_data.get('name', instance.name)
#        instance.created_at = validated_data.get('created_at', instance.created_at)
#        instance.songs.set(validated_data.get('songs', instance.songs))
#
#        instance.save()
#        return instance

class SongsField(serializers.PrimaryKeyRelatedField):

    def to_native(self, value):
        queryset = Song.objects.filter(pk__in=value)
        serializer = SongSerializer(queryset, many=True)
        print(serializer.data)
        return serializer.data

class PlaylistSerializer(serializers.ModelSerializer):
    songs = serializers.PrimaryKeyRelatedField(queryset=Song.objects.all(), many=True, allow_empty=True, required=False)
    #songs = SongsField(queryset=Song.objects.all(), many=True)

    def to_native(self, instance):
        print('heyyyyya')
        ret = super().to_native(instance)
        ret['songs'] = json.loads(ret['songs'])
        return ret
    class Meta:
        model = Playlist
        fields = ['id', 'name', 'songs', 'created_at']