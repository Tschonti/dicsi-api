from django.db import models

# Create your models here.
class Song(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=256)
    lyrics = models.CharField(max_length=5000)
    verses = models.CharField(max_length=5000, blank=True, default='')

    def __str__(self) :
        return '%d. %s' % (self.id, self.title)

class Playlist(models.Model):
    name = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    songs = models.ManyToManyField(Song, through="SongInPlaylist")

    def __str__(self):
        return '%s (%d song(s))' % (self.name, len(self.songs.all()))

class SongInPlaylist(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='order')
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    place = models.IntegerField()

class Search(models.Lookup):
    lookup_name = 'mysearch'

    def as_mysql(self, compiler, connection):
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)
        params = lhs_params + rhs_params
        return 'MATCH (%s) AGAINST (%s IN BOOLEAN MODE)' % (lhs, rhs), params

models.CharField.register_lookup(Search)
models.TextField.register_lookup(Search)