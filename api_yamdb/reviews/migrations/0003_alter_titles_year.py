# Generated by Django 3.2 on 2023-06-13 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_titles_genres'),
    ]

    operations = [
        migrations.AlterField(
            model_name='titles',
            name='year',
            field=models.DateTimeField(verbose_name='Дата произведения'),
        ),
    ]
