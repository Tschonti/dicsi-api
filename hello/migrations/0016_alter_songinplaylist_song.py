# Generated by Django 4.0.1 on 2022-02-01 12:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0015_alter_songinplaylist_song'),
    ]

    operations = [
        migrations.AlterField(
            model_name='songinplaylist',
            name='song',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='place', to='hello.song'),
        ),
    ]
