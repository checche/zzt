# zzt課題

## 開発環境構築手順  
### 環境
Python 3.6.8  
django 2.1.5  
django-allauth 0.39.1  
django-filter 2.1.0  
django-rest-auth 0.9.3  
djangorestframework 3.9.2  

### 手順
1. まず[anaconda](https://www.anaconda.com/)をインストール  
2. 以下のコマンドをターミナルで実行
```
% conda install -c anaconda django  
% conda install -c conda-forge djangorestframework  
% conda install -c auto django-filter
% conda install -c conda-forge django-rest-auth  
% conda install -c conda-forge django-allauth  
% conda install -c conda-forge python-coreapi 
```

## サーバー立ち上げ手順
```
% cd zozo
% python manage.py runserver
```
[http://localhost:8000/](http://localhost:8000/)にサーバが立ち上がる 
## テスト実行手順
以下のコマンドで実行できる.
```
% python manage.py test
```

## curlでの使い方  
ログインが必要な処理にはHTTPヘッダに以下の内容を付加する    
`Authorization: Token {{トークン}}`
### テストユーザー
#### 管理者
adminにアクセス可能  
ID:checche  
ユーザー名:たーくん  
パスワード:testroot
#### 一般ユーザー
ID:hirata  
ユーザー名:ひらたさん  
パスワード:testgeneral

### サインアップ
```
% curl -i -X POST \
   -H "Content-Type:application/json" \
   -d \
'{
    "username": "testboy",
    "email": "testboy@mail.com",
    "password1": "testboy11",
    "password2": "testboy11"
}' \
 'http://localhost:8000/rest-auth/registration/'
```
認証トークンが発行され,ユーザー登録とログインが完了する.
```
{
"key": "9c4a2012e5441b440872c0d7ce8660754345d13f"
}
```

### ログイン
```
% curl -i -X POST \
   -H "Content-Type:application/json" \
   -d \
'{
    "username": "testboy",
    "email": "",
    "password": "testboy11"
}' \
 'http://localhost:8000/rest-auth/login/'
```
認証トークンが発行され,ログインできる.
```
{
"key": "af827a086d6d1a3578e0024c48684c874830501b"
}
```

### ログアウト
```
% curl -i -X POST \
   -H "Authorization:Token af827a086d6d1a3578e0024c48684c874830501b" \
   -H "Content-Type:application/json" \
   -d \
'' \
 'http://localhost:8000/rest-auth/logout/'
```
ログアウトできると以下の内容が返却される.
```
{
"detail": "Successfully logged out."
}
```

### 投稿一覧
```
% curl -i -X GET \
   -H "Authorization:Token 93d8d273ba5d900c840aafb94368aa789cf547bf" \
 'http://localhost:8000/tweets/'
```

### 投稿
```
% curl -i -X POST \
   -H "Authorization:Token 93d8d273ba5d900c840aafb94368aa789cf547bf" \
   -H "Content-Type:application/json" \
   -d \
'{
    "text": "writtenbytestboy2"
}' \
 'http://localhost:8000/tweets/'
```
### 投稿修正
PUTの場合はtextが必須になる.
```
% curl -i -X PUT \
   -H "Authorization:Token 93d8d273ba5d900c840aafb94368aa789cf547bf" \
   -H "Content-Type:application/json" \
   -d \
'{
    "text": "testdesu"
}' \
 'http://localhost:8000/tweets/16/'
```
PATCHの場合textがなくても良い
```
% curl -i -X PATCH \
   -H "Authorization:Token 93d8d273ba5d900c840aafb94368aa789cf547bf" \
   -H "Content-Type:application/json" \
   -d \
'{
    "text": "testdesu"
}' \
 'http://localhost:8000/tweets/16/'
```

### 投稿削除
```
% curl -i -X DELETE \
   -H "Authorization:Token 93d8d273ba5d900c840aafb94368aa789cf547bf" \
 'http://localhost:8000/tweets/15/'
```
## 追加機能
### ユーザー管理・管理者機能 
#### 管理者ユーザー
* ユーザリストの閲覧
* 全ユーザーの情報を閲覧
* 全ユーザーの情報を削除することができる.
#### 非管理ユーザー
* 全ユーザーの情報を閲覧
* 自分の情報の編集ができる  
* 自分の情報の削除ができる 

#### 管理ユーザー作成方法
```
python manage.py createsuperuser
```
管理ユーザーのトークンを用いて以下のコマンドでユーザーリストを確認できる.
```
% curl -i -X GET \
   -H "Authorization:Token 8bc73c04904be8724dd01dacfca6e553c9d4ad2b" \
 'http://localhost:8000/users/'
```

### 投稿のお気に入り登録
以下のようにPOSTすることで投稿をお気に入り登録することができる.
```
% curl -i -X POST \
   -H "Authorization:Token 8bc73c04904be8724dd01dacfca6e553c9d4ad2b" \
   -H "Content-Type:application/json" \
   -d \
'' \
 'http://localhost:8000/tweets/20/fav/'
```
### Core API  
Core APIという機能を使ってスキーマをブラウザ上で確認できる.  
[http://localhost:8000/docs/](http://localhost:8000/docs/)

### トークン認証
django-allauthを使ってトークン認証を実装した.