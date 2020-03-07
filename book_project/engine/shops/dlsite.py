import re
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_binary
#画像保存用
import urllib.request

def get_single_item(driver, obj):
    # タイトルに'DLsite'が含まれていることを確認する。
    assert 'DLsite' in driver.title

    # 商品名を取得
    title_element = driver.find_element_by_xpath('//*[@id="work_name"]/a')
    obj.info.title = title_element.text
    print(obj.info.title)

    # ショップ名称を取得
    shop_name_element = driver.find_element_by_xpath('//*[@id="work_maker"]/tbody/tr/td/span/a')
    obj.info.circle = shop_name_element.text
    print(obj.info.circle)

    # 画像保存
    image_element = driver.find_element_by_xpath("/html/body/div[3]/div[4]/div[1]/div/div[1]/div[1]/div/div/div[2]/div/div[1]/div[1]/ul/li[1]/img") #Unable to locate element:

    # 画像URLを取得
    url = image_element.get_attribute("src")
    print(url)

    # 画像のファイル名を取得
    filename = re.findall(r'https://.*/(RJ.*_img_main\.jpg)', url)
    print(filename[0])

    # 保存用パスを生成
    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    path += "/../media/dlsite/" + filename[0]
    print(path)

    # 画像を保存用パスへダウンロード
    urllib.request.urlretrieve(url, path)

    # DBのパスを更新
    obj.image_path = "dlsite/" + filename[0]