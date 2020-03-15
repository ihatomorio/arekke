import chromedriver_binary
import urllib.request

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from book_app import models
from engine.shops import booth, dlsite, fanza_comic, fanza_doujin, melonbooks

def get_product_info(product):
    # サイト別に取得する
    if 'booth.pm' in product.url:
        booth.get_product_info(product)
    elif 'www.dlsite.com' in product.url:
        dlsite.get_product_info(product)
    elif 'www.melonbooks.co.jp' in product.url:
        melonbooks.get_product_info(product)
    elif 'www.dmm.co.jp/dc/doujin' in product.url:
        fanza_doujin.get_product_info(product)
    elif 'book.dmm.co.jp' in product.url:
        fanza_comic.get_product_info(product)


def get_product_list(account, request):
    # サイト別に取得する
    # if account.shop == models.Account.BOOTH:
        # booth.get_product_list(account, request)
    if account.shop == models.Account.DLSITE:
        dlsite.get_product_list(account, request)
    elif account.shop == models.Account.FANZA_DOUJIN:
        fanza_doujin.get_product_list(account, request)
    elif account.shop == models.Account.MELONBOOKS:
        melonbooks.get_product_list(account, request)
    # elif account.shop == models.Account.FANZA_COMIC:
    #     fanza_comic.get_product_list(account, request)


def close_browser(driver):
    # ブラウザーを終了
    driver.quit()

