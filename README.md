# Arekke - Manage your ecchi book

あれ？この本買ったっけ？な書籍管理アプリです。

## How to install

1. git clone this or Download ZIP and unzip

2. Install packages
    - python3
    - google-chrome
    - ChromeDriver
    - Django
    - django-widget-tweaks
    - pillow
    - django-cleanup

3. Install SB Admin 2

    ```shell for install SB Admin 2
    arekke$ mkdir -p static/bootstrap
    arekke$ cd
    ~$ wget https://github.com/BlackrockDigital/startbootstrap-sb-admin-2/archive/gh-pages.zip
    ~$ unzip gh-pages.zip
    ~$ cp -r startbootstrap-sb-admin-2-gh-pages/* /path/to/arekke/book_project/static/bootstrap
    ```

4. Make migrate

    ```shell
    cd book_project
    python3 manage.py makemigrations
    python3 manage.py migrate
    python3 manage.py createsuperuser
    ```

## Start Server

```shell
sh start_server.sh
```

and you can change port in `start_server.sh` file

## Open Web Page

You can get access for `localhost:8080`

## Developing Environment Versions

```shell
$ python --version
Python 3.6.9

$ google-chrome --version
Google Chrome 81.0.4044.34 beta
$ chromedriver --version
ChromeDriver 81.0.4044.69 (6813546031a4bc83f717a2ef7cd4ac6ec1199132-refs/branch-heads/4044@{#776})

$ python
Python 3.6.9 (default, Nov  7 2019, 10:44:02)
[GCC 8.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import django
>>> print(django.get_version())
3.0.4
```
