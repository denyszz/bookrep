# Generated by Django 4.2.8 on 2023-12-27 05:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_book_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='author',
            field=models.CharField(default='Unknown', max_length=5),
        ),
    ]
