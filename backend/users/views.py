from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, Post, Like, Comment, Chat, Message, Topic
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core import serializers
from .serializers import (
    UserSerializer,
    PostSerializer,
    LikeSerializer,
    CommentSerializer,
    ChatSerializer,
    MessageSerializer,
    TopicSerializer,
)
import json

from django.contrib.auth.hashers import make_password
from rest_framework import status


class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        # Get the raw password from the request data
        raw_password = self.request.data.get('password')

        if raw_password:
            # Hash the password
            hashed_password = make_password(raw_password)

            # Create the user with the hashed password
            serializer.save(password=hashed_password)
        else:
            raise serializers.ValidationError({'password': 'Password is required'})


class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class TopicListCreateView(generics.ListCreateAPIView):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer


class PostListCreateView(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            subscribed_topics = user.topics_of_interest.all()
            return Post.objects.filter(topic__in=subscribed_topics).order_by('-created_at')
        return Post.objects.none()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class LikeListCreateView(generics.ListCreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class LikeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer


class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class ChatListCreateView(generics.ListCreateAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]


class ChatRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer


class MessageListCreateView(generics.ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)


class MessageRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


class SubscribeToTopicView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        topic_name = request.data.get('topic_name')
        if not topic_name:
            return JsonResponse({"error": "Topic name is required."}, status=400)

        topic = get_object_or_404(Topic, name=topic_name)
        user = request.user
        user.topics_of_interest.add(topic)
        user.save()

        return JsonResponse({"message": f"Subscribed to {topic_name}"}, status=200)


class FollowingListAPIView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return user.following.all()
        return User.objects.none()


class UserTopicsListAPIView(generics.ListAPIView):
    serializer_class = TopicSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return user.topics_of_interest.all()
        return Topic.objects.none()


class UserPostsListAPIView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.kwargs['pk']
        return Post.objects.filter(user__id=user_id).order_by('-created_at')


@csrf_exempt
def login_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")

        print(f"Username: {username}, Password: {password}")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            return JsonResponse({"message": "Logged in successfully.", "access": access_token}, status=200)
        else:
            print("User authentication failed")
            return JsonResponse({"message": "Invalid credentials."}, status=401)
    else:
        return JsonResponse({"message": "Method not allowed."}, status=405)


@login_required
def subscribed_feed(request):
    topics = request.user.profile.topics_subscribed.all()
    posts = Post.objects.filter(topic__in=topics).order_by('-created_at')
    post_list = serializers.serialize('json', posts)
    return JsonResponse(post_list, safe=False)
