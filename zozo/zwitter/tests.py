from django.test import TestCase
from .models import CustomUser, Tweet
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate, APITestCase, APIClient
from .views import CustomUserViewSet, TweetViewSet
import json
from rest_framework.authtoken.models import Token
import pytz
import datetime
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

class UserListTest(APITestCase):
    """ユーザーリスト"""
    def setUp(self):
        """初期化"""
         #認証管理ユーザー作成(test_user_1)
        CustomUser.objects.create(username='test1', screenname='T1', email='test1@test1.com', password='user1', is_staff=True)
        self.test_user_1 = CustomUser.objects.get(username='test1')
        self.admin_client = APIClient()
        self.admin_client.force_authenticate(user=self.test_user_1)
        #認証ユーザー作成(test_user_2)
        CustomUser.objects.create(username='test2', screenname='T2',email='test2@test2.com', password='user2', is_staff=False)
        self.test_user_2 = CustomUser.objects.get(username='test2')
        self.auth_client = APIClient()
        self.auth_client.force_authenticate(user=self.test_user_2)
        #未認証ユーザー
        self.client = APIClient()

        Tweet.objects.create(text='i am test1', author=self.test_user_1)
        Tweet.objects.create(text='i am test2', author=self.test_user_2)
        

    def tearDown(self):
        """終了処理"""

    def test_list(self):
        """管理ユーザーがユーザー一覧を見れるか"""
        #管理ユーザー
        response = self.admin_client.get('/users/', format='json')
        expected = {
            "count": 2,
            "next": None,
            "previous": None,
            "results": [
                {
                    "pk": 1,
                    "username": "test1",
                    "screenname": "T1",
                    "email": "test1@test1.com",
                    "is_staff": True,
                    "tweets": [
                        1
                    ],
                    "favorite": [
                    ]
                },
                {
                    "pk": 2,
                    "username": "test2",
                    "screenname": "T2",
                    "email": "test2@test2.com",
                    "is_staff": False,
                    "tweets": [
                        2
                    ],
                    "favorite": [
                    ]
                }
            ]
        }

        self.assertEqual(json.loads(response.content), expected)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        #認証ユーザー
        response2 = self.auth_client.get('/users/', format='json')
        self.assertEqual(response2.status_code, status.HTTP_403_FORBIDDEN)
        #未認証ユーザー
        response3 = self.client.get('/users/', format='json')
        self.assertEqual(response3.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve(self):
        """ユーザーが個別の情報を見ることができるか"""
        #管理ユーザー
        response = self.admin_client.get('/users/1/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.admin_client.get('/users/2/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        #認証ユーザー
        response2 = self.auth_client.get('/users/1/', format='json')
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        response2 = self.auth_client.get('/users/2/', format='json')
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        #未認証ユーザー
        response3 = self.client.get('/users/2/', format='json')
        self.assertEqual(response3.status_code, status.HTTP_403_FORBIDDEN)

    def test_partial_update(self):
        """本人のみがpartial_updateできるか"""
        #管理者本人
        response = self.admin_client.patch('/users/1/', json.dumps({"screenname": "renamed"}), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(CustomUser.objects.count(), 2)
        self.assertEqual(CustomUser.objects.get(pk=1).screenname, 'renamed')
        #管理者が本人以外を編集
        response = self.admin_client.put('/users/2/', json.dumps({"screenname": "renamed"}), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        #認証ユーザー本人
        response2 = self.auth_client.patch('/users/2/', json.dumps({"screenname": "renamed"}), content_type='application/json')
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(CustomUser.objects.count(), 2)
        self.assertEqual(CustomUser.objects.get(pk=2).screenname, 'renamed')
        #認証ユーザーが本人以外を編集
        response2 = self.auth_client.put('/users/1/', json.dumps({"screenname": "renamed"}), content_type='application/json')
        self.assertEqual(response2.status_code, status.HTTP_403_FORBIDDEN)
        #未認証ユーザー
        response3 = self.client.put('/users/1/', json.dumps({"screenname": "renamed"}), content_type='application/json')
        self.assertEqual(response3.status_code, status.HTTP_403_FORBIDDEN)


    def test_update(self):
        """本人のみがupdateできるか"""
        #管理者本人
        response = self.admin_client.put(
            '/users/1/', 
            json.dumps({
                "username": "renamed1",
                "screenname": "R1",
                "email": "renamed1@renamed1.com",
            }), 
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(CustomUser.objects.count(), 2)
        self.assertEqual(CustomUser.objects.get(pk=1).screenname, 'R1')
        #管理者が本人以外を編集
        response = self.admin_client.put(
            '/users/2/', 
            json.dumps({
                "username": "renamed2",
                "screenname": "R2",
                "email": "renamed2@renamed2.com",
            }), 
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        #認証ユーザー本人
        response2 = self.auth_client.put(
            '/users/2/', 
            json.dumps({
                "username": "renamed2",
                "screenname": "R2",
                "email": "renamed2@renamed2.com",
            }), 
            content_type='application/json'
        )
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(CustomUser.objects.count(), 2)
        self.assertEqual(CustomUser.objects.get(pk=2).screenname, 'R2')
        #認証ユーザーが本人以外を編集
        response2 = self.auth_client.put(
            '/users/1/', 
            json.dumps({
                "username": "renamed1",
                "screenname": "R1",
                "email": "renamed1@renamed1.com",
            }), 
            content_type='application/json'
        )
        self.assertEqual(response2.status_code, status.HTTP_403_FORBIDDEN)
        #未認証ユーザー
        response3 = self.client.put(
            '/users/1/', 
            json.dumps({
                "username": "renamed1",
                "screenname": "R1",
                "email": "renamed1@renamed1.com",
            }), 
            content_type='application/json'
        )
        self.assertEqual(response3.status_code, status.HTTP_403_FORBIDDEN)


    def test_delete(self):
        """管理者と本人のみがdeleteできるか"""
        CustomUser.objects.create(username='test3', screenname='T3',email='test3@test3.com', password='user3', is_staff=False)
        #未認証ユーザー
        response3 = self.client.delete('/users/3/')
        self.assertEqual(response3.status_code, status.HTTP_403_FORBIDDEN)
        #認証ユーザー本人以外
        response2 = self.auth_client.delete('/users/3/')
        self.assertEqual(response2.status_code, status.HTTP_403_FORBIDDEN)
        #認証ユーザー本人
        response2 = self.auth_client.delete('/users/2/')
        self.assertEqual(response2.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(CustomUser.objects.count(), 2)
        #管理ユーザー
        response = self.admin_client.delete('/users/3/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(CustomUser.objects.count(), 1)
        #管理ユーザー本人
        response = self.admin_client.delete('/users/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(CustomUser.objects.count(), 0)

class TweetTest(APITestCase):
    """短文投稿について"""
    def setUp(self):
        """初期化"""
        CustomUser.objects.create(username='test1', screenname='T1', email='test1@test1.com', password='user1')
        CustomUser.objects.create(username='test2', screenname='T2',email='test2@test2.com', password='user2')
        CustomUser.objects.create(username='test3', screenname='T3',email='test3@test3.com', password='user3')
        self.test_user_1 = CustomUser.objects.get(username='test1')
        self.test_user_2 = CustomUser.objects.get(username='test2')
        self.test_user_3 = CustomUser.objects.get(username='test3')
        #認証ユーザー作成(test_user_1)
        self.auth_client = APIClient()
        self.auth_client.force_authenticate(user=self.test_user_1)
        Tweet.objects.create(text='i am test1', author=self.test_user_1)
        Tweet.objects.create(text='i am test2', author=self.test_user_2)
        Tweet.objects.create(text='i am test3', author=self.test_user_3)
        #未認証ユーザー
        self.client = APIClient()

    def tearDown(self):
        """終了処理"""


    def test_create(self):
        """認証済みユーザーがcreateできるか"""
        response = self.auth_client.post(
            '/tweets/', 
            json.dumps({
                "text": "created by test1"
            }), 
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Tweet.objects.count(), 4)
        self.assertEqual(Tweet.objects.get(pk=4).text, 'created by test1')

        response2 = self.client.post(
            '/tweets/', 
            json.dumps({
                "text": "created by test1"
            }), 
            content_type='application/json'
        )
        self.assertEqual(response2.status_code, status.HTTP_403_FORBIDDEN)


    def test_list(self):
        """
        認証済みユーザーが自分以外の投稿一覧を見れるか
        test_user_1がリストを取得した時1番目に出てくる投稿は
        test_user_2の投稿になっているはず
        """
        response = self.auth_client.get('/tweets/', format='json')
        results = response.data['results']
        first_tweet = results[0]
        # restframeworkのテスト環境でdatetimeを取得するとタイムゾーンがUTCになるバグがある
        test2_created_at = Tweet.objects.get(pk=2).created_at
        test3_created_at = Tweet.objects.get(pk=3).created_at
        # その修正をする
        test2_ca_fixed = test2_created_at.replace(tzinfo=datetime.timezone(datetime.timedelta(hours=9))) + datetime.timedelta(hours=9)
        created2=test2_ca_fixed.isoformat(sep='T')
        test3_ca_fixed = test3_created_at.replace(tzinfo=datetime.timezone(datetime.timedelta(hours=9))) + datetime.timedelta(hours=9)
        created3=test3_ca_fixed.isoformat(sep='T')

        expected = {
            "count": 2,
            "next": None,
            "previous": None,
            "results": [
                {
                    "pk": 2,
                    "author": "T2 @test2",
                    "text": "i am test2",
                    "created_at": created2,
                    "favorite_by": []
                },
                {
                    "pk": 3,
                    "author": "T3 @test3",
                    "text": "i am test3",
                    "created_at": created3,
                    "favorite_by": []
                }
            ]
        }

        
        self.assertEqual(json.loads(response.content), expected)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        #未認証ユーザー
        response2 = self.client.get('/tweets/', format='json')
        self.assertEqual(response2.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve(self):
        """認証ユーザーが個別の短文を見ることができるか"""
        #認証ユーザー
        response = self.auth_client.get('/tweets/1/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        #未承認ユーザー
        response2 = self.client.get('/tweets/1/', format='json')
        self.assertEqual(response2.status_code, status.HTTP_403_FORBIDDEN)


    def test_update(self):
        """著者のみがupdateできるか"""
        response = self.auth_client.put(
            '/tweets/1/', 
            json.dumps({
                "text": "updated by test1"
                }
            ), 
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Tweet.objects.count(), 3)
        self.assertEqual(Tweet.objects.get(pk=1).text, 'updated by test1')
        #未認証ユーザー
        response2 = self.client.put(
            '/tweets/1/', 
            json.dumps({
                "text": "updated by test1"
                }
            ), 
            content_type='application/json'
        )
        self.assertEqual(response2.status_code, status.HTTP_403_FORBIDDEN)
        #著者ではない認証ユーザー
        response3 = self.auth_client.put(
            '/tweets/2/', 
            json.dumps({
                "text": "updated by test1"
                }
            ), 
            content_type='application/json'
        )
        self.assertEqual(response3.status_code, status.HTTP_403_FORBIDDEN)


    def test_partial_update(self):
        """
        著者のみがpartial_updateできるか
        本文しか更新内容が無いので,空jsonを投入
        """
        #著者
        response = self.auth_client.patch('/tweets/1/', json.dumps({}), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Tweet.objects.count(), 3)
        self.assertEqual(Tweet.objects.get(pk=1).text, 'i am test1')
        #未認証ユーザー
        response2 = self.client.put('/tweets/1/', json.dumps({}), content_type='application/json')
        self.assertEqual(response2.status_code, status.HTTP_403_FORBIDDEN)
        #著者ではない認証ユーザー
        response3 = self.auth_client.put('/tweets/2/', json.dumps({}), content_type='application/json')
        self.assertEqual(response3.status_code, status.HTTP_403_FORBIDDEN)


    def test_delete(self):
        """著者のみがdeleteできるか"""
        #未認証ユーザー
        response2 = self.client.delete('/tweets/1/')
        self.assertEqual(response2.status_code, status.HTTP_403_FORBIDDEN)
        #著者ではない認証ユーザー
        response3 = self.auth_client.delete('/tweets/2/')
        self.assertEqual(response3.status_code, status.HTTP_403_FORBIDDEN)
        #著者
        response = self.auth_client.delete('/tweets/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Tweet.objects.count(), 2)

    def test_favorite(self):
        """認証ユーザーがお気に入り登録できるか"""
        response = self.auth_client.post('/tweets/1/fav/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response2 = self.auth_client.get('/tweets/1/', format='json')
        self.assertEqual(response2.data['favorite_by'], [1])
        #未認証ユーザー
        response3 = self.client.post('/tweets/1/fav/')
        self.assertEqual(response3.status_code, status.HTTP_403_FORBIDDEN)
