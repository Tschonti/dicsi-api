# Generated by Django 4.0.1 on 2022-01-31 13:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0009_songinplaylist_alter_playlist_songs_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='songinplaylist',
            name='playlist',
        ),
        migrations.RemoveField(
            model_name='songinplaylist',
            name='song',
        ),
        migrations.DeleteModel(
            name='Playlist',
        ),
        migrations.DeleteModel(
            name='SongInPlaylist',
        ),
    ]
