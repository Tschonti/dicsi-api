from django.db import models

# Create your models here.
class Song(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=256)
    lyrics = models.CharField(max_length=5000)
    verses = models.CharField(max_length=5000, blank=True, default='')
