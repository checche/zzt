from django.shortcuts import render
import django_filters
from rest_framework import viewsets, filters, generics, permissions, status
from .models import CustomUser, Tweet
from .serializer import CustomUserSerializer, TweetSerializer
from .permissions import IsAuthorOrReadOnly
from rest_framework.response import Response

class CustomUserViewSet(viewsets.ModelViewSet):
    """ユーザー情報"""
    permission_classes = (permissions.IsAdminUser,)
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

class TweetViewSet(viewsets.ModelViewSet):
    """ツイート情報"""
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer
    filter_fields = ('author', 'text')

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