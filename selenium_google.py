from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_binary

#画像保存用
import urllib.request

# ブラウザーを起動
options = Options()
options.binary_location = '/opt/google/chrome-beta/google-chrome-beta'
options.add_argument('--headless')
options.add_argument('--no-sandbox') #rootに必要
driver = webdriver.Chrome(options=options)

# Webページにアクセス
driver.get('https://www.google.co.jp/')

# タイトルに'Google'が含まれていることを確認する。
assert 'Google' in driver.title

# htmlを取得・表示
html = driver.page_source
print(html)

# スクリーンショットを撮る。
driver.save_screenshot('google_screenshot.png')

# ブラウザーを終了
driver.quit()