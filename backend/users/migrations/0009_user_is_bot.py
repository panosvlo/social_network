# Generated by Django 4.2 on 2023-05-27 22:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0008_article_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_bot',
            field=models.BooleanField(default=False),
        ),
    ]
