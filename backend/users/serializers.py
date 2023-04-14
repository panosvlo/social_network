from rest_framework import serializers
from .models import User, Post, Like, Comment, Chat, Message, Topic


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    topics_of_interest = TopicSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'topics_of_interest')


class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    topic_name = serializers.CharField(write_only=True, required=True)
    topic = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'user', 'content', 'created_at', 'topic', 'topic_name')

    def create(self, validated_data):
        topic_name = validated_data.pop('topic_name')
        topic, _ = Topic.objects.get_or_create(name=topic_name)
        post = Post.objects.create(topic=topic, **validated_data)
        return post


class LikeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Like
        fields = ('id', 'user', 'post', 'created_at')


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'user', 'post', 'content', 'created_at')


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ('id', 'chat', 'sender', 'content', 'created_at')


class ChatSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Chat
        fields = ('id', 'participants', 'created_at', 'messages')
