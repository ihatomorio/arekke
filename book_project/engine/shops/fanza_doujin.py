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
    # title_element = driver.find_element_by_class_name("u-text-wrap u-tpg-title1 u-mt-0 u-mb-400") #spacing NG
    # title_element = driver.find_element_by_css_selector(".u-text-wrap.u-tpg-title1.u-mt-0.u-mb-400") # countermeasure spacing
    title_element = driver.find_element_by_css_selector('#doujinLIst > div.l-areaMainColumn > div.l-areaProductTitle > div.m-productHeader > div > div > div.m-productInfo > div > div > div > div > h1')
    # title_element = driver.find_element_by_xpath('//*[@id="doujinLIst"]/div[2]/div[1]/div[1]/div/div/div[2]/div/div/div/div/h1')
    # title_element = driver.find_element_by_css_selector("body > div.page-wrap > main > div.market-item-detail.u-bg-white > article > div > div.u-bg-white.u-pt-600.u-px-700 > div.container > div > div.u-order-1.l-col-2of5.u-pl-600 > header > h2") # works but long...
    obj.info.title = title_element.text
    print(obj.info.title)

    # サークル名称を取得
    # shop_name_element = driver.find_element_by_class_name("u-text-ellipsis")
    shop_name_element = driver.find_element_by_xpath('//*[@id="doujinLIst"]/div[2]/div[1]/div[2]/div/div[1]/div/div/div/a')
    obj.info.circle = shop_name_element.text
    print(obj.info.circle)


    # 画像保存
    image_element = driver.find_element_by_xpath('//*[@id="fn-slides"]/li[1]/a/img') #Unable to locate element:
    # image_element = driver.find_element_by_css_selector('body > div.page-wrap > main > div.market-item-detail.u-bg-white > article > div > div.u-bg-white.u-pt-600.u-px-700 > div.container > div > div.u-order-0.l-col-3of5.u-pr-500 > div.primary-image-area.slick-initialized.slick-slider > div > div > div.slick-slide.slick-current.slick-active > div > div > div > img') #OK
    # image_element = driver.find_element_by_class_name("market-item-detail-item-image") #None
    # image_element = driver.find_element_by_css_selector(".market-item-detail-item-image") #None

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
