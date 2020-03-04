from django.db import models

class Book(models.Model):
    # 書名
    title = models.CharField(max_length=256)
    # 著者
    author = models.CharField(max_length=256)
    # サークル名
    circle = models.CharField(max_length=256)


class Product(models.Model):

    # 店舗の定数
    NONE = 0
    
    BOOTH = 10
    DLSITE = 20
    FANZA_COMIC = 30
    FANZA_DOUJIN = 31
    MELONBOOKS = 40
    TORANOANA = 50
    
    # 書籍情報
    info = models.ForeignKey('Book', on_delete=models.CASCADE)
    # 購入店舗
    shop = models.IntegerField()
    # URL
    url = models.URLField(max_length=512)
    # 購入日時
    date = models.DateTimeField(null=True, blank=True)