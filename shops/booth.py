from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_binary
#画像保存用
import urllib.request

def get_single_item(driver):
    # タイトルに'BOOTH'が含まれていることを確認する。
    assert 'BOOTH' in driver.title

    # 商品名を取得
    # title_element = driver.find_element_by_class_name("u-text-wrap u-tpg-title1 u-mt-0 u-mb-400") #spacing NG
    title_element = driver.find_element_by_css_selector(".u-text-wrap.u-tpg-title1.u-mt-0.u-mb-400") # countermeasure spacing
    # title_element = driver.find_element_by_css_selector("body > div.page-wrap > main > div.market-item-detail.u-bg-white > article > div > div.u-bg-white.u-pt-600.u-px-700 > div.container > div > div.u-order-1.l-col-2of5.u-pl-600 > header > h2") # works but long...
    print(title_element.text)

    # ショップ名称を取得
    shop_name_element = driver.find_element_by_class_name("u-text-ellipsis")
    print(shop_name_element.text)

    # 画像保存
    # image_element = driver.find_element_by_xpath("/html/body/div[2]/main/div[2]/article/div/div[2]/div[1]/div/div[2]/div[1]/div/div/div[2]/div/div/div/img") #Unable to locate element:
    image_element = driver.find_element_by_css_selector('body > div.page-wrap > main > div.market-item-detail.u-bg-white > article > div > div.u-bg-white.u-pt-600.u-px-700 > div.container > div > div.u-order-0.l-col-3of5.u-pr-500 > div.primary-image-area.slick-initialized.slick-slider > div > div > div.slick-slide.slick-current.slick-active > div > div > div > img') #OK
    # image_element = driver.find_element_by_class_name("market-item-detail-item-image") #None
    # image_element = driver.find_element_by_css_selector(".market-item-detail-item-image") #None

    url = image_element.get_attribute("src")

    print(url)

    assert 'resized' in url

    urllib.request.urlretrieve(url, 'image.png')
