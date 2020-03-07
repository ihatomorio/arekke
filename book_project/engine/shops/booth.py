import re
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_binary
#画像保存用
import urllib.request

def get_single_item(driver, obj):
    # タイトルに'BOOTH'が含まれていることを確認する。
    assert 'BOOTH' in driver.title

    # 商品名を取得
    title_element = driver.find_element_by_css_selector(".u-text-wrap.u-tpg-title1.u-mt-0.u-mb-400") # countermeasure spacing
    obj.info.title = title_element.text
    print(obj.info.title)

    # ショップ名称を取得
    shop_name_element = driver.find_element_by_class_name("u-text-ellipsis")
    obj.info.circle = shop_name_element.text
    print(obj.info.circle)

    # 画像保存
    image_element = driver.find_element_by_css_selector('body > div.page-wrap > main > div.market-item-detail.u-bg-white > article > div > div.u-bg-white.u-pt-600.u-px-700 > div.container > div > div.u-order-0.l-col-3of5.u-pr-500 > div.primary-image-area.slick-initialized.slick-slider > div > div > div.slick-slide.slick-current.slick-active > div > div > div > img') #OK

    # 画像URLを取得
    url = image_element.get_attribute("src")
    print(url)

    # 画像のファイル名を取得
    filename = re.findall(r'https://.*/(.*_base_resized\.jpg)', url)
    print(filename[0])

    # 保存用パスを生成
    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    path += "/../media/booth/" + filename[0]
    print(path)

    # 画像を保存用パスへダウンロード
    urllib.request.urlretrieve(url, path)

    # DBのパスを更新
    obj.image_path = "booth/" + filename[0]
