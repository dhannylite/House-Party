# Generated by Django 4.0.5 on 2022-06-28 14:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spotify', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='SortifyToken',
            new_name='SpotifyToken',
        ),
    ]
