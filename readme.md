#zzt課題

## 開発環境構築手順  
[anaconda](https://www.anaconda.com/)をインストール  
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
python manage.py runserver
```

## テスト実行手順

## curlでの使い方  
### ログイン
```
curl -i -X POST \
   -H "Content-Type:application/json" \
   -d \
'{
    "username": "maco",
    "email": "",
    "password": "Timeout47"
}' \
 'http://localhost:8000/rest-auth/login/'
```
```
{
"key": "48aea51237c7e51f1f2e6704668020e52e4f378b"
}
```
が返却

### ログアウト
```
curl -i -X POST \
   -H "Content-Type:application/json" \
   -d \
'' \
 'http://localhost:8000/rest-auth/logout/'
```

### サインアップ
```
curl -i -X POST \
   -H "Content-Type:application/json" \
   -d \
'{
    "username": "testboy3",
    "email": "testboy3@gmail.com",
    "password1": "Timeout47",
    "password2": "Timeout47"
}' \
 'http://localhost:8000/rest-auth/registration/'
```

```
{
"key": "bd351e024fac9225c98d8cca2b59105eb6e926de"
}
```
