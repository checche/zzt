# zzt課題

## 開発環境構築手順  
1. まず[anaconda](https://www.anaconda.com/)をインストール  
2. 以下のコマンドをターミナルで実行
```
conda install -c anaconda django  
conda install -c conda-forge djangorestframework  
conda install -c auto django-filter
conda install -c conda-forge django-rest-auth  
conda install -c conda-forge django-allauth  
conda install -c conda-forge python-coreapi 
```

## サーバー立ち上げ手順
```
cd zozo
python manage.py runserver
```

## テスト実行手順
テストコードはすでに完成しているので,以下のコマンドで実行すれば良い.
```
python manage.py test
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
curl -i -X POST \
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
curl -i -X POST \
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
curl -i -X POST \
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
curl -i -X GET \
   -H "Authorization:Token 93d8d273ba5d900c840aafb94368aa789cf547bf" \
 'http://localhost:8000/tweets/'
```

### 投稿
```
curl -i -X POST \
   -H "Authorization:Token 93d8d273ba5d900c840aafb94368aa789cf547bf" \
   -H "Content-Type:application/json" \
   -d \
'{
    "text": "writtenbytestboy2",
    "favorite_by": []
}' \
 'http://localhost:8000/tweets/'
```
### 投稿修正
```
curl -i -X PATCH \
   -H "Authorization:Token 93d8d273ba5d900c840aafb94368aa789cf547bf" \
   -H "Content-Type:application/json" \
   -d \
'{
    "pk": 16,
    "author": 8,
    "text": "testdesu",
    "created_at": "2019-04-09T01:50:20.456007+09:00",
    "favorite_by": []
}' \
 'http://localhost:8000/tweets/16/'
```

### 投稿削除
```
curl -i -X DELETE \
   -H "Authorization:Token 93d8d273ba5d900c840aafb94368aa789cf547bf" \
 'http://localhost:8000/tweets/15/'
```
## 追加機能
