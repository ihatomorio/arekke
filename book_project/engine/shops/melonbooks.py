import re
import chromedriver_binary
import time
#画像保存用
import urllib.request

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from django.conf import settings

from book_app import views
from book_app.models import Product

def get_product_info(product):
    # ブラウザーを起動
    options = Options()
    options.binary_location = '/opt/google/chrome-beta/google-chrome-beta'
    options.add_argument('--headless')
    options.add_argument('--no-sandbox') #rootに必要
    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(60)

    # Webページにアクセス
    driver.get(product.url)

    # タイトルに'メロンブックス'が含まれていることを確認する。
    assert 'メロンブックス' in driver.title

    try:
        if 'ご指定のページはございません。' in driver.find_element_by_css_selector('body > div.box-warning-01 > p').text:
            print(driver.find_element_by_css_selector('body > div.box-warning-01 > p').text)
    except NoSuchElementException:
        pass

    try:
        # 商品名を取得
        product.title = driver.find_element_by_xpath('//*[@id="description"]/table/tbody/tr[1]/td').text
        print(product.title)
    except NoSuchElementException:
        pass
    try:
        # サークル名称を取得
        product.circle = driver.find_element_by_css_selector('#title > div > div > div.clm_g > div > a').text
        print(product.circle)
    except NoSuchElementException:
        pass
    try:
        # 作家名を取得
        product.author = driver.find_element_by_xpath('//*[@id="description"]/table/tbody/tr[3]/td/a').text
        print(product.author)
    except NoSuchElementException:
        pass
    try:
        # 画像URLを取得
        url = driver.find_element_by_class_name('tag_sample1').get_attribute("href")
        print(url)

        # 画像のファイル名を取得
        filename = re.findall(r'https://.*image=(.*\.jpg)', url)
        print(filename[0])

        # 保存用パスを生成 MEDIA_ROOT = '/root/repos/websq/book_project/media'
        path = settings.MEDIA_ROOT + "/melonbooks/" + filename[0]
        print(path)

        # 画像を保存用パスへダウンロード
        urllib.request.urlretrieve(url, path)

        # DBのパスを更新
        product.image_path = "melonbooks/" + filename[0]
        
    except NoSuchElementException:
        print('element error!')

    # shop番号を更新
    product.shop = Product.MELONBOOKS
    
    # ブラウザを閉じる
    driver.quit()


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
    while True:
        product_elements = driver.find_elements_by_class_name('product')
        for product_element in product_elements:
            inner_html = product_element.get_attribute("innerHTML")
            # print(inner_html)
            infos = re.findall(r'<p class="name"><a href="(/detail/detail.php\?product_id=\d+)" title="商品番号:\d+ .*">商品番号:\d+<br>(.*)</a></p>', inner_html)
            print(infos[0][0]) #URL
            print(infos[0][1]) #title
            if views.CreateFromUrl('https://www.melonbooks.co.jp' + infos[0][0], request) == -1:
                pass
        try:
            # driver.find_element_by_xpath('//*[@id="container"]/div/div[1]/div/div[6]/div/ul/li[3]/a/span').click
            elements = driver.find_elements_by_class_name('next')
            for element in elements:
                if '次へ' in element.text:
                    print(element.text)
                    element.click
            # driver.implicitly_wait(3)
            time.sleep(15)
            driver.save_screenshot('page_screenshot.png')
            break
            # WebDriverWait(driver, 15).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, 'product')))
        except NoSuchElementException:
            print('no button')
            break
        except TimeoutException:
            print('timed out')
            break

    print('finished')

    # ブラウザを閉じる
    driver.quit()