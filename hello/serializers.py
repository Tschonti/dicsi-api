from rest_framework import serializers

from .models import Song

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