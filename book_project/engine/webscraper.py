from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_binary
from book_app import models
from . import shops

def get_product_info(product):
    # サイト別に取得する
    if 'booth.pm' in product.url:
        shops.booth.get_product_info(product)
    elif 'www.dlsite.com' in product.url:
        shops.dlsite.get_product_info(product)
    elif 'www.melonbooks.co.jp' in product.url:
        shops.melonbooks.get_product_info(product)
    elif 'www.dmm.co.jp/dc/doujin' in product.url:
        shops.fanza_doujin.get_product_info(product)
    elif 'book.dmm.co.jp' in product.url:
        shops.fanza_comic.get_product_info(product)


def get_product_list(account, request):
    # サイト別に取得する
    # if account.shop == models.Account.BOOTH:
        # shops.booth.get_product_list(account, request)
    if account.shop == models.Account.DLSITE:
        shops.dlsite.get_product_list(account, request)
    elif account.shop == models.Account.FANZA_DOUJIN:
        shops.fanza_doujin.get_product_list(account, request)
    # elif account.shop == models.Account.FANZA_COMIC:
    #     shops.fanza_comic.get_product_list(account, request)
    # elif account.shop == models.Account.MELONBOOKS:
    #     shops.melonbooks.get_product_list(account, request)


def close_browser(driver):
    # ブラウザーを終了
    driver.quit()