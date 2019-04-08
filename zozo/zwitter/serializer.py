from rest_framework import serializers
from .models import CustomUser, Tweet
from rest_auth.serializers import UserDetailsSerializer

class CustomUserSerializer(UserDetailsSerializer):
    class Meta:
        model = CustomUser
        fields = ('pk', 'username', 'screenname', 'email', 'is_staff')

class TweetSerializer(serializers.ModelSerializer):
    # author = CustomUserSerializer(read_only=True)
    # user_id = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), write_only=True)
    class Meta:
        model = Tweet
        read_only_fields = ('created_at',)
        fields = ('pk', 'author', 'text', 'created_at', 'favorite_by')
    """
    def create(self, validated_date):
        validated_date['author'] = validated_date.get('user_id', None)
        if validated_date['author'] is None:
            raise serializers.ValidationError("user not found.") 
        del validated_date['user_id']
        return Tweet.objects.create(**validated_date)
    """