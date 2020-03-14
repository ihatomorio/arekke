import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
import chromedriver_binary
from django.conf import settings
from engine import webscraper
#画像保存用
import urllib.request
from book_app.models import Product
from book_app import views

def get_product_info(product):
    # ブラウザーを起動
    options = Options()
    options.binary_location = '/opt/google/chrome-beta/google-chrome-beta'
    options.add_argument('--headless')
    options.add_argument('--no-sandbox') #rootに必要
    driver = webdriver.Chrome(options=options)

    # Webページにアクセス
    driver.get(product.url)

    # タイトルに'FANZA同人'が含まれていることを確認する。
    assert 'FANZA同人' in driver.title

    # 商品名を取得
    title_element = driver.find_element_by_css_selector('#doujinLIst > div.l-areaMainColumn > div.l-areaProductTitle > div.m-productHeader > div > div > div.m-productInfo > div > div > div > div > h1')
    product.title = title_element.text
    print(product.title)

    # サークル名称を取得
    shop_name_element = driver.find_element_by_xpath('//*[@id="doujinLIst"]/div[2]/div[1]/div[2]/div/div[1]/div/div/div/a')
    product.circle = shop_name_element.text
    print(product.circle)


    # 画像保存
    image_element = driver.find_element_by_xpath('//*[@id="fn-slides"]/li[1]/a/img') #Unable to locate element:

    # 画像URLを取得
    url = image_element.get_attribute("src")
    print(url)

    # 画像のファイル名を取得
    filename = re.findall(r'https://.*/(.*\.jpg)', url)
    print(filename[0])

    # 保存用パスを生成 MEDIA_ROOT = '/root/repos/websq/book_project/media'
    path = settings.MEDIA_ROOT + "/fanza_doujin/" + filename[0]
    print(path)

    # 画像を保存用パスへダウンロード
    urllib.request.urlretrieve(url, path)

    # DBのパスを更新
    product.image_path = "fanza_doujin/" + filename[0]

    # shop番号を更新
    product.shop = Product.FANZA_DOUJIN
    
    # ブラウザを閉じる
    webscraper.close_browser(driver)

   
def get_product_list(account, request):
    # ブラウザーを起動
    options = Options()
    options.binary_location = '/opt/google/chrome-beta/google-chrome-beta'
    options.add_argument('--headless')
    options.add_argument('--no-sandbox') #rootに必要
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(800, 800)

    # Webページにアクセス
    list_page = 'https://www.dmm.co.jp/dc/-/mylibrary/'
    driver.get(list_page)
    
    # スクリーンショットを撮る。
    driver.save_screenshot('page_screenshot.png')

    # ログインされているか確認
    try:
        page_title_element = driver.find_element_by_css_selector("#mylibrary-app > div > div:nth-child(1) > div.localListArea12vtK > div.headerTitleList1LTRN > h1")
        print(page_title_element.text)
    except NoSuchElementException:
        # されていなければログイン
        print("not logged in")

        user_id_element = driver.find_element_by_name("login_id")
        user_id_element.send_keys(account.user)
        password_element = driver.find_element_by_name("password")
        password_element.send_keys(account.password)
        
        # ログインボタンを押す
        driver.find_element_by_css_selector('#loginbutton_script_on > span').click()

        # Webページにアクセス
        # driver.get('https://www.dmm.co.jp/dc/-/mylibrary/')
        
        wait = WebDriverWait(driver, 10)
        wait.until(lambda driver: driver.current_url == "https://www.dmm.co.jp/dc/-/mylibrary/")
            
        # スクリーンショットを撮る。
        driver.save_screenshot('page_screenshot.png')

        try:
            page_title_element = driver.find_element_by_css_selector("#mylibrary-app > div > div:nth-child(1) > div.localListArea12vtK > div.headerTitleList1LTRN > h1")
        except NoSuchElementException:
            print("login failed")
            return None

    # 表からURLとタイトル一覧の取得し保存
    product_elements = driver.find_elements_by_class_name('localListProduct1pSCw')
    for product_element in product_elements:
        inner_html = product_element.get_attribute("innerHTML")
        print(inner_html)
        infos = re.findall(r'<a href=\"/dc/-/mylibrary/detail/=/product_id=(.*/)\".*<p>(.*)</p></div><p', inner_html)
        if infos:
            print('https://www.dmm.co.jp/dc/doujin/-/detail/=/cid=' + infos[0][0]) #URL
            print(infos[0][1]) #title
            # URL: https://www.dmm.co.jp/dc/doujin/-/detail/=/cid=d_065087/
            # href:                     /dc/-/mylibrary/detail/=/product_id=d_065087/
            if views.CreateFromUrl('https://www.dmm.co.jp/dc/doujin/-/detail/=/cid=' + infos[0][0], request) == -1:
                break

    # ブラウザを閉じる
    webscraper.close_browser(driver)