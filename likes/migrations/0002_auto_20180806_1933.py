# Generated by Django 2.0.7 on 2018-08-06 11:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('likes', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='likecount',
            old_name='Liked_num',
            new_name='liked_num',
        ),
    ]
