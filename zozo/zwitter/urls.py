from django.urls import path, include
from . import views
from rest_framework import routers
from .views import CustomUserViewSet, TweetViewSet, Favorite


app_name = 'zwitter'

router = routers.DefaultRouter()

router.register('users', CustomUserViewSet)
router.register('tweets', TweetViewSet)

urlpatterns = [
    path('tweets/<int:tweet_pk>/fav/', Favorite),
]

urlpatterns += router.urls
