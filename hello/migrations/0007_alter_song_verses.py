# Generated by Django 3.2.5 on 2021-07-26 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0006_song_verses'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='verses',
            field=models.CharField(blank=True, default='', max_length=5000),
        ),
    ]
