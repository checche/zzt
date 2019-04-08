from django.urls import path, include
from . import views
from rest_framework import routers
from .views import CustomUserViewSet, TweetViewSet


app_name = 'zwitter'

router = routers.DefaultRouter()

router.register('users', CustomUserViewSet)
router.register('tweets', TweetViewSet)