# Generated by Django 3.2 on 2023-06-16 08:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0016_auto_20230616_1125'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='review',
            unique_together={('title_id', 'author')},
        ),
    ]
