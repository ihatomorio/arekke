import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import chromedriver_binary
from selenium.webdriver.support.ui import Select
from django.conf import settings
from engine import webscraper
#画像保存用
import urllib.request
# DB操作
from book_app.models import Book, Product
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

    # タイトルに'DLsite'が含まれていることを確認する。
    assert 'DLsite' in driver.title

    # 商品名を取得
    title_element = driver.find_element_by_xpath('//*[@id="work_name"]/a')
    product.info.title = title_element.text
    print(product.info.title)

    # ショップ名称を取得
    shop_name_element = driver.find_element_by_xpath('//*[@id="work_maker"]/tbody/tr/td/span/a')
    product.info.circle = shop_name_element.text
    print(product.info.circle)

    # 画像保存
    image_element = driver.find_element_by_xpath("/html/body/div[3]/div[4]/div[1]/div/div[1]/div[1]/div/div/div[2]/div/div[1]/div[1]/ul/li[1]/img") #Unable to locate element:

    # 画像URLを取得
    url = image_element.get_attribute("src")
    print(url)

    # 画像のファイル名を取得
    filename = re.findall(r'https://.*/(RJ.*_img_main\.jpg)', url)
    print(filename[0])

    # 保存用パスを生成 MEDIA_ROOT = '/root/repos/websq/book_project/media'
    path = settings.MEDIA_ROOT + "/dlsite/" + filename[0]
    print(path)

    # 画像を保存用パスへダウンロード
    urllib.request.urlretrieve(url, path)

    # DBのパスを更新
    product.image_path = "dlsite/" + filename[0]

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
    list_page = 'https://www.dlsite.com/maniax/mypage/userbuy/complete'
    driver.get(list_page)

    # ログインされているか確認
    try:
        page_title_element = driver.find_element_by_css_selector("#main_inner > div.base_title > h1")
        print(page_title_element.text)
    except NoSuchElementException:
        # されていなければログイン
        print("not logged in")

        # ログイン画面を開く
        driver.get('https://login.dlsite.com/login')

        user_id_element = driver.find_element_by_name("login_id")
        user_id_element.send_keys(account.user)
        password_element = driver.find_element_by_name("password")
        password_element.send_keys(account.password)
        
        # driver.find_element_by_class_name("btn__type-clrDefault__type-sizeMd").click()
        # /html/body/div[2]/div/div/section/div[2]/div[1]/div[1]/div/form/div[3]/button
        driver.find_element_by_css_selector('body > div.l-container > div > div > section > div.mainBox-body > div.contentBox > div:nth-child(1) > div > form > div.loginBtn > button').click()
        
        # 18歳以上です
        driver.find_element_by_css_selector('body > div.adult_check_box._adultcheck > div > ul > li.btn_yes.btn-approval > a').click()

    # Webページにアクセス
    driver.get('https://www.dlsite.com/maniax/mypage/userbuy/complete')

    # 購入月:すべて を選択
    select_elemet = Select(driver.find_element_by_id('_start'))
    select_elemet.select_by_value('all')

    # 表示 をクリック
    driver.find_element_by_id('_display').click()
    
    # スクリーンショットを撮る。
    driver.save_screenshot('page_screenshot.png')

    # 表からURLとタイトル一覧の取得し保存
    product_elements = driver.find_elements_by_class_name('work_name')
    for product_element in product_elements:
        inner_html = product_element.get_attribute("innerHTML")
        infos = re.findall(r' +<a href="(http.*\.html)">(.*)</a>', inner_html)
        print(infos[0][0]) #URL
        print(infos[0][1]) #title
        if views.CreateFromUrl(infos[0][0], request) == -1:
            break

    # ブラウザを閉じる
    webscraper.close_browser(driver)