import re, os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_binary
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

    # タイトルに'メロンブックス'が含まれていることを確認する。
    assert 'メロンブックス' in driver.title

    # 商品名を取得
    title_element = driver.find_element_by_xpath('//*[@id="title"]/div/div[1]/div[1]/h1')
    obj.info.title = title_element.text
    print(obj.info.title)

    # サークル名称を取得
    shop_name_element = driver.find_element_by_xpath('//*[@id="title"]/div/div[2]/div[1]/div/a')
    obj.info.circle = shop_name_element.text
    print(obj.info.circle)

    # 作家名を取得
    author_element = driver.find_element_by_xpath('//*[@id="description"]/table/tbody/tr[3]/td/a')
    obj.info.author = author_element.text
    print(obj.info.author)

    # 画像保存
    image_element = driver.find_element_by_xpath('//*[@id="main"]/div[1]/a/img')

    # 画像URLを取得
    url = image_element.get_attribute("src")
    print(url)

    # 画像のファイル名を取得
    filename = re.findall(r'https://.*image=(.*\.jpg).*', url)
    print(filename[0])

    # 保存用パスを生成
    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    path += "/../media/melonbooks/" + filename[0]
    print(path)

    # 画像を保存用パスへダウンロード
    urllib.request.urlretrieve(url, path)

    # DBのパスを更新
    obj.image_path = "melonbooks/" + filename[0]
    
    # ブラウザを閉じる
    webscraper.close_browser(driver)
