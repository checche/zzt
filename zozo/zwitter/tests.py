from django.test import TestCase
from .models import CustomUser, Tweet
from rest_framework.test import APIRequestFactory, force_authenticate
from .views import CustomUserViewSet, TweetViewSet

# Create your tests here.
class CustomUserTest(TestCase):
    def setup(self):
        """初期化"""
        CustomUser.objects.create_user(username='Test', password='test1')

    

class TweetTest(TestCase):
    def setUp(self):
        """初期化"""
        test_user = CustomUser.objects.create_user(username='Test', password='test1')
        Tweet.objects.create(text='test', author=test_user)
        self.view = TweetViewSet.as_view()

    def tearDown(self):
        """終了処理"""

    def test_create(self):
        """認証(ログイン)済みユーザーがcreateできるか"""
        factory = APIRequestFactory()
        auth_user = CustomUser.objects.get(username='Authenticated')
        
        request = factory.post(
            'tweets/',
            {
                
            },
            format='json')
        force_authenticate(request, user=auth_user)
        response = view(request)

    def test_read(self):
        """認証(ログイン)済みユーザーがreadできるか"""

    def test_update(self):
        """著者と管理者のみがupdateできるか"""

    def test_delete(self):
        """著者と管理者のみがdeleteできるか"""