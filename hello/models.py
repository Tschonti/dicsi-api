from django.db import models

# Create your models here.
class Song(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=256)
    lyrics = models.CharField(max_length=5000)
    verses = models.CharField(max_length=5000, blank=True, default='')

class Playlist(models.Model):
    name = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    songs = models.ManyToManyField(Song, through="SongInPlaylist")

class SongInPlaylist(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    place = models.IntegerField()
