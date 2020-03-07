import re
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_binary

#画像保存用
import urllib.request

def get_single_item(driver, obj):
    # タイトルに'FANZA同人'が含まれていることを確認する。
    assert 'FANZA同人' in driver.title

    # 商品名を取得
    title_element = driver.find_element_by_css_selector('#doujinLIst > div.l-areaMainColumn > div.l-areaProductTitle > div.m-productHeader > div > div > div.m-productInfo > div > div > div > div > h1')
    obj.info.title = title_element.text
    print(obj.info.title)

    # サークル名称を取得
    shop_name_element = driver.find_element_by_xpath('//*[@id="doujinLIst"]/div[2]/div[1]/div[2]/div/div[1]/div/div/div/a')
    obj.info.circle = shop_name_element.text
    print(obj.info.circle)


    # 画像保存
    image_element = driver.find_element_by_xpath('//*[@id="fn-slides"]/li[1]/a/img') #Unable to locate element:

    # 画像URLを取得
    url = image_element.get_attribute("src")
    print(url)

    # 画像のファイル名を取得
    filename = re.findall(r'https://.*/(.*\.jpg)', url)
    print(filename[0])

    # 保存用パスを生成
    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    path += "/../media/fanza_doujin/" + filename[0]
    print(path)

    # 画像を保存用パスへダウンロード
    urllib.request.urlretrieve(url, path)

    # DBのパスを更新
    obj.image_path = "fanza_doujin/" + filename[0]
