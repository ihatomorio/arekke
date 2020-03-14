import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
import chromedriver_binary
from django.conf import settings
from engine import webscraper
#画像保存用
import urllib.request
from book_app.models import Product
from book_app import views


def GetProductTitleFromDriver(driver):
    return driver.find_element_by_xpath('//*[@id="title"]/div/div[1]/div[1]/h1').text


def GetProductCircleFromDriver(driver):
    return driver.find_element_by_xpath('//*[@id="title"]/div/div[2]/div[1]/div/a').text


def GetProductAuthorFromDriver(driver):
    return driver.find_element_by_xpath('//*[@id="description"]/table/tbody/tr[3]/td/a').text


def GetProductImageUrlFromDriver(driver):
    return driver.find_element_by_xpath('//*[@id="main"]/div[1]/a/img').get_attribute("src")


def get_product_info(product):
    # ブラウザーを起動
    options = Options()
    options.binary_location = '/opt/google/chrome-beta/google-chrome-beta'
    options.add_argument('--headless')
    options.add_argument('--no-sandbox') #rootに必要
    driver = webdriver.Chrome(options=options)

    # Webページにアクセス
    driver.get(product.url)

    # タイトルに'メロンブックス'が含まれていることを確認する。
    assert 'メロンブックス' in driver.title

    # 商品名を取得
    product.title = GetProductTitleFromDriver(driver)
    print(product.title)

    # サークル名称を取得
    product.circle = GetProductCircleFromDriver(driver)
    print(product.circle)

    # 作家名を取得
    product.author = GetProductAuthorFromDriver(driver)
    print(product.author)

    # 画像URLを取得
    url = GetProductImageUrlFromDriver(driver)
    print(url)

    # 画像のファイル名を取得
    filename = re.findall(r'https://.*image=(.*\.jpg).*', url)
    print(filename[0])

    # 保存用パスを生成 MEDIA_ROOT = '/root/repos/websq/book_project/media'
    path = settings.MEDIA_ROOT + "/melonbooks/" + filename[0]
    print(path)

    # 画像を保存用パスへダウンロード
    urllib.request.urlretrieve(url, path)

    # DBのパスを更新
    product.image_path = "melonbooks/" + filename[0]
    
    # shop番号を更新
    product.shop = Product.MELONBOOKS
    
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
    list_page = 'https://www.melonbooks.co.jp/mypage/history.php'
    driver.get(list_page)

    # ログインされているか確認
    try:
        page_title_element = driver.find_element_by_css_selector("#container > div > div.clm_g > div > div.headline.head_l.mb20 > div > h1")
        print(page_title_element.text)
    except NoSuchElementException:
        # されていなければログイン
        print("not logged in")

        # ログイン情報を入力
        user_id_element = driver.find_element_by_id("melonbooks_login_id")
        user_id_element.send_keys(account.user)
        password_element = driver.find_element_by_id("melonbooks_password")
        password_element.send_keys(account.password)
        
        # ログインボタンをクリック
        driver.find_element_by_css_selector('#login_mypage > table > tbody > tr:nth-child(2) > td > div > input:nth-child(2)').click()

        try:
            page_title_element = driver.find_element_by_css_selector("#container > div > div.clm_g > div > div.headline.head_l.mb20 > div > h1")
            print(page_title_element.text)
        except NoSuchElementException:
            # されていなければログイン
            print("login failed")
            
    # 注文時期:すべて を選択
    select_elemet = Select(driver.find_element_by_name('search_select'))
    select_elemet.select_by_value('999')

    # スクリーンショットを撮る。
    driver.save_screenshot('page_screenshot.png')

    # GO をクリック
    driver.find_element_by_css_selector('#form1 > div > div > div > div.clm.clm_r > span.input_btn.br_5 > a').click()
    
    # スクリーンショットを撮る。
    driver.save_screenshot('page_screenshot.png')

    # 表からURLとタイトル一覧の取得し保存
    product_elements = driver.find_elements_by_class_name('product')
    for product_element in product_elements:
        inner_html = product_element.get_attribute("innerHTML")
        # print(inner_html)
        infos = re.findall(r'<p class="name"><a href="(/detail/detail.php\?product_id=\d+)" title="商品番号:\d+ .*">商品番号:\d+<br>(.*)</a></p>', inner_html)
        print(infos[0][0]) #URL
        print(infos[0][1]) #title
        if views.CreateFromUrl('https://www.melonbooks.co.jp' + infos[0][0], request) == -1:
            break

    # ブラウザを閉じる
    webscraper.close_browser(driver)