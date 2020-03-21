# 前提パッケージのバージョン確認結果

```shell
mikan@sana:~/arekke$ python --version
Python 3.6.9

mikan@sana:~/arekke$ google-chrome --version
Google Chrome 80.0.3987.132 

mikan@sana:~/arekke$ chromedriver --version
ChromeDriver 80.0.3987.16 (320f6526c1632ad4f205ebce69b99a062ed78647-refs/branch-heads/3987@{#185})

mikan@sana:~/arekke$ python
Python 3.6.9 (default, Nov  7 2019, 10:44:02) 
[GCC 8.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import django
>>> print(django.get_version())
3.0.4

mikan@sana:~/arekke$ python -m django --version
3.0.4
```

# プロジェクトの追加

```shell
mikan@sana:~/arekke$ django-admin startproject book_project
```

# ログインの追加


# サーバー起動方法
抜けると終了してしまうので、forkerを使いましょう。
```
forker 'sh start_server.sh'
```
