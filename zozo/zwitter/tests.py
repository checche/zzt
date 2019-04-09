from django.test import TestCase
from .models import CustomUser, Tweet
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate, APITestCase, APIClient
from .views import CustomUserViewSet, TweetViewSet
import json
from rest_framework.authtoken.models import Token

class CustomUserTest(APITestCase):
    """ユーザーについて"""
    def setup(self):
        """初期化"""
        CustomUser.objects.create(username='test1', email='test1@test1.com', password='user1')
        CustomUser.objects.create(username='test2', email='test2@test2.com', password='user2')
        self.test_user_1 = CustomUser.objects.get(username='test1')
        self.test_user_2 = CustomUser.objects.get(username='test2')
        self.client = APIClient()

    def test_signup(self):
        """サインアップ"""
        response = self.client.post('/rest-auth/registration/',
            json.dumps({"username": "testboy",
            "email": "testboy@mail.com",
            "password1": "testboy11",
            "password2": "testboy11"}),
            content_type='application/json')
        self.assertTrue(response.data['key'])

    def test_signup_logout(self):
        """サインアップしてログアウト"""
        #signup
        response = self.client.post('/rest-auth/registration/',
            json.dumps({"username": "testboy",
            "email": "testboy@mail.com",
            "password1": "testboy11",
            "password2": "testboy11"}),
            content_type='application/json')
        token = response.data['key']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        #logout
        response2 = self.client.post('/rest-auth/logout/',content_type='application/json')
        self.assertEqual(response2.status_code, status.HTTP_200_OK)

class TweetTest(APITestCase):
    """短文投稿について"""
    def setUp(self):
        """初期化"""
        CustomUser.objects.create(username='test1', email='test1@test1.com', password='user1')
        CustomUser.objects.create(username='test2', email='test2@test2.com', password='user2')
        CustomUser.objects.create(username='test3', email='test2@test3.com', password='user3')
        self.test_user_1 = CustomUser.objects.get(username='test1')
        self.test_user_2 = CustomUser.objects.get(username='test2')
        self.test_user_3 = CustomUser.objects.get(username='test3')
        #認証ユーザー作成(test_user_1)
        self.auth_client = APIClient()
        self.auth_client.force_authenticate(user=self.test_user_1)
        Tweet.objects.create(text='i am test1', author=self.test_user_1)
        Tweet.objects.create(text='i am test2', author=self.test_user_2)
        Tweet.objects.create(text='i am test3', author=self.test_user_3)

        self.client = APIClient()

    def tearDown(self):
        """終了処理"""

    def test_create(self):
        """認証済みユーザーがcreateできるか"""
        response = self.auth_client.post(
            '/tweets/', 
            json.dumps({
                "text": "created by test1",
                "favorite_by": []
            }), 
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Tweet.objects.count(), 4)
        self.assertEqual(Tweet.objects.get(pk=4).text, 'created by test1')

        response2 = self.client.post(
            '/tweets/', 
            json.dumps({
                "text": "created by test1",
                "favorite_by": []
            }), 
            content_type='application/json'
        )
        self.assertEqual(response2.status_code, status.HTTP_403_FORBIDDEN)

    def test_read(self):
        """
        認証済みユーザーが自分以外の投稿一覧を見れるか
        test_user_1がリストを取得した時1番目に出てくる投稿は
        test_user_2の投稿になっているはず
        """
        response = self.auth_client.get('/tweets/', format='json')
        results = response.data['results']
        first_tweet = results[0]
        self.assertEqual(first_tweet['pk'], 2)
        self.assertEqual(first_tweet['author']['pk'], 2)
        self.assertEqual(first_tweet['text'], 'i am test2')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response2 = self.client.get('/tweets/', format='json')
        self.assertEqual(response2.status_code, status.HTTP_403_FORBIDDEN)

    def test_update(self):
        """著者のみがpartial_updateできるか"""
        response = self.auth_client.put(
            '/tweets/1/', 
            json.dumps({
                "text": "updated by test1",
                "favorite_by": [2,3]}
            ), 
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Tweet.objects.count(), 3)
        self.assertEqual(Tweet.objects.get(pk=1).text, 'updated by test1')
        response2 = self.client.put(
            '/tweets/1/', 
            json.dumps({
                "text": "updated by test1",
                "favorite_by": [2,3]}
            ), 
            content_type='application/json'
        )
        self.assertEqual(response2.status_code, status.HTTP_403_FORBIDDEN)

    def test_partial_update(self):
        """著者のみがpartial_updateできるか"""
        response = self.auth_client.patch('/tweets/1/', json.dumps({"favorite_by": [2,3]}), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Tweet.objects.count(), 3)
        self.assertEqual(Tweet.objects.get(pk=1).text, 'i am test1')
        response2 = self.client.put('/tweets/1/', json.dumps({"favorite_by": [2,3]}), content_type='application/json')
        self.assertEqual(response2.status_code, status.HTTP_403_FORBIDDEN)


    def test_delete(self):
        """著者のみがdeleteできるか"""
        response = self.auth_client.delete('/tweets/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Tweet.objects.count(), 2)

        response2 = self.auth_client.delete('/tweets/2/')
        self.assertEqual(response2.status_code, status.HTTP_403_FORBIDDEN)