# Generated by Django 2.0.7 on 2018-07-28 06:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0014_readdetail'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='readdetail',
            name='blog',
        ),
        migrations.DeleteModel(
            name='ReadDetail',
        ),
    ]
