from rest_framework import serializers
from .models import CustomUser, Tweet
from rest_auth.serializers import UserDetailsSerializer

class CustomUserSerializer(UserDetailsSerializer):
    class Meta:
        model = CustomUser
        fields = ('pk', 'username', 'screenname', 'email', 'is_staff')

class TweetSerializer(serializers.ModelSerializer):
    # author = CustomUserSerializer()
    # favorite_by = CustomUserSerializer()
    class Meta:
        model = Tweet
        read_only_fields = ('created_at',)
        fields = ('pk','author', 'text', 'created_at', 'favorite_by')
