from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_binary
from book_app import models
from . import shops

def get_single_item(obj):
    # ブラウザーを起動
    options = Options()
    options.binary_location = '/opt/google/chrome-beta/google-chrome-beta'
    options.add_argument('--headless')
    options.add_argument('--no-sandbox') #rootに必要
    driver = webdriver.Chrome(options=options)

    # Webページにアクセス
    driver.get(obj.url)

    # サイト別に取得する
    if 'booth.pm' in obj.url:
        shops.booth.get_single_item(driver, obj)
    elif 'www.dlsite.com' in obj.url:
        shops.dlsite.get_single_item(driver, obj)
    elif 'www.melonbooks.co.jp' in obj.url:
        shops.melonbooks.get_single_item(driver, obj)
    elif 'www.dmm.co.jp/dc/doujin' in obj.url:
        shops.fanza_doujin.get_single_item(driver, obj)
    elif 'book.dmm.co.jp' in obj.url:
        shops.fanza_comic.get_single_item(driver, obj)

    # ブラウザーを終了
    driver.quit()