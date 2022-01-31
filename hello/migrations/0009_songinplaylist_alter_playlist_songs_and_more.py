# Generated by Django 4.0.1 on 2022-01-31 12:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0008_playlist'),
    ]

    operations = [
        migrations.CreateModel(
            name='SongInPlaylist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('place', models.IntegerField()),
            ],
        ),
        migrations.AlterField(
            model_name='playlist',
            name='songs',
            field=models.ManyToManyField(through='hello.SongInPlaylist', to='hello.Song'),
        ),
        migrations.AddField(
            model_name='songinplaylist',
            name='playlist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hello.playlist'),
        ),
        migrations.AddField(
            model_name='songinplaylist',
            name='song',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hello.song'),
        ),
    ]