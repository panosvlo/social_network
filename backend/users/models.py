from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class User(AbstractUser):
    email = models.EmailField(unique=True)
    topics_of_interest = models.ManyToManyField('Topic', related_name='interested_users')
    following = models.ManyToManyField('self', symmetrical=False, related_name='followers', blank=True)


class Topic(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(default="null")


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='posts')
    likes = models.ManyToManyField(User, related_name="liked_posts", blank=True)

    @property
    def comments_count(self):
        return self.comments.count()


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.content}"


class Chat(models.Model):
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='chats')
    created_at = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Article(models.Model):
    url = models.URLField(max_length=2048)
    title = models.CharField(max_length=255, default="null")
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='articles')
    source = models.CharField(max_length=255)
