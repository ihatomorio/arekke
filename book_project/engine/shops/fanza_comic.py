import re
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_binary
#画像保存用
import urllib.request

def get_single_item(driver, obj):
    # タイトルに'FANZA電子書籍'が含まれていることを確認する。
    assert 'FANZA電子書籍' in driver.title

    # 商品名を取得
    title_element = driver.find_element_by_css_selector('#title')
    obj.info.title = title_element.text
    print(obj.info.title)

    # 作者を取得
    shop_name_element = driver.find_element_by_class_name("m-boxDetailProductInfoMainList__description__list")
    obj.info.author = shop_name_element.text
    print(obj.info.author)
    
    # シリーズ名を取得
    obj.info.circle = ""
    print(obj.info.circle)

    # 画像保存
    image_element = driver.find_element_by_class_name("m-imgDetailProductPack") #None

    # 画像URLを取得
    url = image_element.get_attribute("src")
    print(url)

    # 画像のファイル名を取得
    filename = re.findall(r'https://.*/(.*\.jpg)', url)
    print(filename[0])

    # 保存用パスを生成
    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    path += "/../media/fanza_comic/" + filename[0]
    print(path)

    # 画像を保存用パスへダウンロード
    urllib.request.urlretrieve(url, path)

    # DBのパスを更新
    obj.image_path = "fanza_comic/" + filename[0]
