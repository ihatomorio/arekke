import re, os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import chromedriver_binary
from engine import webscraper
#画像保存用
import urllib.request

def get_product_info(product):
    # ブラウザーを起動
    options = Options()
    options.binary_location = '/opt/google/chrome-beta/google-chrome-beta'
    options.add_argument('--headless')
    options.add_argument('--no-sandbox') #rootに必要
    driver = webdriver.Chrome(options=options)

    # Webページにアクセス
    driver.get(product.url)

    # タイトルに'BOOTH'が含まれていることを確認する。
    assert 'BOOTH' in driver.title

    # 商品名を取得
    title_element = driver.find_element_by_css_selector(".u-text-wrap.u-tpg-title1.u-mt-0.u-mb-400") # countermeasure spacing
    product.info.title = title_element.text
    print(product.info.title)

    # ショップ名称を取得
    shop_name_element = driver.find_element_by_class_name("u-text-ellipsis")
    product.info.circle = shop_name_element.text
    print(product.info.circle)

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
    product.image_path = "booth/" + filename[0]

    # ブラウザを閉じる
    webscraper.close_browser(driver)


def get_product_list(account, request):
    # ブラウザーを起動
    options = Options()
    options.binary_location = '/opt/google/chrome-beta/google-chrome-beta'
    options.add_argument('--headless')
    options.add_argument('--no-sandbox') #rootに必要
    driver = webdriver.Chrome(options=options)

    # Webページにアクセス
    list_page = 'https://accounts.booth.pm/orders'
    driver.get(list_page)

    # ログインされているか確認
    try:
        page_title_element = driver.find_element_by_class_name("manage-page-head-title")
        print(page_title_element.text)
    except NoSuchElementException:
        # されていなければログイン
        print("not logged in")
        # スクリーンショットを撮る。
        driver.save_screenshot('page_screenshot.png')

    # 一覧へ行く

    # ブラウザを閉じる
    webscraper.close_browser(driver)