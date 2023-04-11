from django.urls import path
from .views import (
    UserListCreateView,
    UserRetrieveUpdateDestroyView,
    TopicListCreateView,
    PostListCreateView,
    PostRetrieveUpdateDestroyView,
    LikeListCreateView,
    LikeRetrieveUpdateDestroyView,
    CommentListCreateView,
    CommentRetrieveUpdateDestroyView,
    ChatListCreateView,
    ChatRetrieveUpdateDestroyView,
    MessageListCreateView,
    MessageRetrieveUpdateDestroyView,
)

urlpatterns = [
    path('users/', UserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', UserRetrieveUpdateDestroyView.as_view(), name='user-retrieve-update-destroy'),
    path('topics/', TopicListCreateView.as_view(), name='topic-list-create'),
    path('posts/', PostListCreateView.as_view(), name='post-list-create'),
    path('posts/<int:pk>/', PostRetrieveUpdateDestroyView.as_view(), name='post-retrieve-update-destroy'),
    path('likes/', LikeListCreateView.as_view(), name='like-list-create'),
    path('likes/<int:pk>/', LikeRetrieveUpdateDestroyView.as_view(), name='like-retrieve-update-destroy'),
    path('comments/', CommentListCreateView.as_view(), name='comment-list-create'),
    path('comments/<int:pk>/', CommentRetrieveUpdateDestroyView.as_view(), name='comment-retrieve-update-destroy'),
    path('chats/', ChatListCreateView.as_view(), name='chat-list-create'),
    path('chats/<int:pk>/', ChatRetrieveUpdateDestroyView.as_view(), name='chat-retrieve-update-destroy'),
    path('messages/', MessageListCreateView.as_view(), name='message-list-create'),
    path('messages/<int:pk>/', MessageRetrieveUpdateDestroyView.as_view(), name='message-retrieve-update-destroy'),
]
