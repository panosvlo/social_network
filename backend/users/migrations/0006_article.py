# Generated by Django 4.2 on 2023-05-22 17:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0005_alter_comment_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField()),
                ('source', models.CharField(max_length=255)),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='articles',
                                            to='users.topic')),
            ],
        ),
    ]