# Generated by Django 4.2 on 2023-05-22 18:52

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0006_article'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='url',
            field=models.URLField(max_length=2048),
        ),
    ]
