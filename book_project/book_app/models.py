from django.conf import settings
from django.db import models
from django.utils import timezone

# 買ったもの
class Product(models.Model):

    # 店舗の定数
    NONE = 0
    BOOTH = 10
    DLSITE = 20
    FANZA_COMIC = 30
    FANZA_DOUJIN = 31
    MELONBOOKS = 40
    TORANOANA = 50

    # 店舗の定数
    SHOPS = (
        (NONE, "なし"),
        (BOOTH, "BOOTH"),
        (DLSITE, "DLSite"),
        (FANZA_COMIC, "FANZA電子書籍"),
        (FANZA_DOUJIN, "FANZA同人"),
        (MELONBOOKS, "メロンブックス"),
    )
    
    # 所有者
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # 書名
    title = models.CharField(max_length=256)
    # 著者
    author = models.CharField(max_length=256)
    # サークル名
    circle = models.CharField(max_length=256)
    # 購入店舗
    shop = models.IntegerField(choices=SHOPS)
    # URL
    url = models.URLField(max_length=512)
    # 購入日時
    date = models.DateTimeField(null=True, blank=True)
    # 追加日時
    added_date = models.DateTimeField(default=timezone.now)
    # 画像のパス
    image_path = models.ImageField(upload_to='uploads/', blank=True)

    # 自身の情報
    def __str__(self):
        return self.title.__str__()

        
# 店舗情報
class Account(models.Model):

    # 店舗の定数
    NONE = 0
    BOOTH = 10
    DLSITE = 20
    FANZA_COMIC = 30
    FANZA_DOUJIN = 31
    MELONBOOKS = 40
    TORANOANA = 50

    # 店舗の定数
    SHOPS = (
        (NONE, "なし"),
        (BOOTH, "BOOTH"),
        (DLSITE, "DLSite"),
        (FANZA_COMIC, "FANZA電子書籍"),
        (FANZA_DOUJIN, "FANZA同人"),
        (MELONBOOKS, "メロンブックス"),
    )
    
    # 所有者
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # サイト
    shop = models.IntegerField(choices=SHOPS)

    # ユーザー名
    user = models.CharField(max_length=256)
    # パスワード
    password = models.CharField(max_length=256)

    # 最終取得日時
    date = models.DateTimeField(null=True, blank=True)