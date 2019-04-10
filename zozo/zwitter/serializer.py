from rest_framework import serializers
from .models import CustomUser, Tweet
from rest_auth.serializers import UserDetailsSerializer

class CustomUserSerializer(UserDetailsSerializer):
    class Meta:
        model = CustomUser
        read_only_fields = ('is_staff', 'tweets', 'favorite')
        fields = ('pk', 'username', 'screenname', 'email', 'is_staff', 'tweets', 'favorite')

class TweetSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Tweet
        read_only_fields = ('author', 'created_at', 'favorite_by')
        fields = ('pk', 'author', 'text', 'created_at', 'favorite_by')
