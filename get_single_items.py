from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_binary

import shops

def get_single_item(url):
    # ブラウザーを起動
    options = Options()
    options.binary_location = '/opt/google/chrome-beta/google-chrome-beta'
    options.add_argument('--headless')
    options.add_argument('--no-sandbox') #rootに必要
    driver = webdriver.Chrome(options=options)

    # Webページにアクセス
    driver.get(url)

    # タイトルを表示
    print(driver.title)

    # URLを表示
    print(driver.current_url)

    # スクリーンショットを撮る。
    driver.save_screenshot('page_screenshot.png')

    # サイト別に取得する
    if 'booth.pm' in url:
        shops.booth.get_single_item(driver)
    elif 'www.dlsite.com' in url:
        shops.dlsite.get_single_item(driver)
    elif 'www.melonbooks.co.jp' in url:
        shops.melonbooks.get_single_item(driver)
    elif 'www.dmm.co.jp/dc/doujin' in url:
        shops.fanza_doujin.get_single_item(driver)
    elif 'book.dmm.co.jp' in url:
        shops.fanza_comic.get_single_item(driver)

    # ブラウザーを終了
    driver.quit()