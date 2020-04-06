# Arekke - Have I bought this book?

あれ？この本買ったっけ？な書籍管理アプリです。

## 動作確認をした前提パッケージのバージョン確認結果

```shell
$ python --version
Python 3.6.9

$ google-chrome --version
Google Chrome 80.0.3987.132 

$ chromedriver --version
ChromeDriver 80.0.3987.16 (320f6526c1632ad4f205ebce69b99a062ed78647-refs/branch-heads/3987@{#185})

$ python
Python 3.6.9 (default, Nov  7 2019, 10:44:02) 
[GCC 8.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import django
>>> print(django.get_version())
3.0.4
```

## Deploy

git clone this

and install SB Admin 2

```shell for install SB Admin 2
arekke$ mkdir -p static/bootstrap
arekke$ cd
~$ wget https://github.com/BlackrockDigital/startbootstrap-sb-admin-2/archive/gh-pages.zip
~$ unzip gh-pages.zip
~$ cp -r startbootstrap-sb-admin-2-gh-pages/* /path/to/arekke/book_project/static/bootstrap
```

## サーバー起動方法

```shell
sh start_server.sh
```
