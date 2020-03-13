import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import chromedriver_binary
from django.conf import settings
from engine import webscraper
#画像保存用
import urllib.request

def get_product_info(obj):
    # ブラウザーを起動
    options = Options()
    options.binary_location = '/opt/google/chrome-beta/google-chrome-beta'
    options.add_argument('--headless')
    options.add_argument('--no-sandbox') #rootに必要
    driver = webdriver.Chrome(options=options)

    # Webページにアクセス
    driver.get(obj.url)

    # タイトルに'FANZA電子書籍'が含まれていることを確認する。
    assert 'FANZA電子書籍' in driver.title

    # 商品名を取得
    title_element = driver.find_element_by_css_selector('#title')
    obj.title = title_element.text
    print(obj.title)

    # 作者を取得
    shop_name_element = driver.find_element_by_class_name("m-boxDetailProductInfoMainList__description__list")
    obj.info.author = shop_name_element.text
    print(obj.info.author)
    
    # シリーズ名を取得
    obj.circle = ""
    print(obj.circle)

    # 画像保存
    image_element = driver.find_element_by_class_name("m-imgDetailProductPack") #None

    # 画像URLを取得
    url = image_element.get_attribute("src")
    print(url)

    # 画像のファイル名を取得
    filename = re.findall(r'https://.*/(.*\.jpg)', url)
    print(filename[0])

    # 保存用パスを生成 MEDIA_ROOT = '/root/repos/websq/book_project/media'
    path = settings.MEDIA_ROOT + "/fanza_comic/" + filename[0]
    print(path)
    
    # 画像を保存用パスへダウンロード
    urllib.request.urlretrieve(url, path)

    # DBのパスを更新
    obj.image_path = "fanza_comic/" + filename[0]
    
    # ブラウザを閉じる
    webscraper.close_browser(driver)