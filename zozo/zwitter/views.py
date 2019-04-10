from django.shortcuts import render
import django_filters
from rest_framework import viewsets, filters, generics, permissions, status
from .models import CustomUser, Tweet
from .serializer import CustomUserSerializer, TweetSerializer
from .permissions import IsAuthorOrReadOnly, IsUserOrReadOnly, IsUserOrAdmin
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

class CustomUserViewSet(viewsets.ModelViewSet):
    """ユーザー情報"""
    # permission_classes = ()
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    
    def get_permissions(self):
        """パーミッションをメソッドによって変える"""
        if self.action in ('retrieve', 'destroy'):
            permission_classes = [permissions.IsAuthenticated, IsUserOrAdmin]
        elif self.action in ('update', 'partial_update'):
            permission_classes = [IsUserOrReadOnly]
        else:
            permission_classes = [permissions.IsAdminUser]
        
        return [permission() for permission in permission_classes]

class TweetViewSet(viewsets.ModelViewSet):
    """ツイート情報"""
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer
    filter_fields = ('text',)

    def get_permissions(self):
        """パーミッションをメソッドによって変える"""
        if self.action in ('list', 'create', 'retrieve'):
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [IsAuthorOrReadOnly]
        return [permission() for permission in permission_classes]

    def list(self, request, *args, **kwargs):
        """自分以外のツイートのリストを取得する"""
        queryset = self.filter_queryset(self.get_queryset().exclude(author=request.user.pk))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def Favorite(request, tweet_pk):
    """短文をお気に入り登録する"""
    favorite_tweet = Tweet.objects.get(pk=tweet_pk)
    favorite_tweet.favorite_by.add(request.user)
    return Response({"message": "favorite tweet number {}".format(tweet_pk), "data": request.data})
    