import re
import time

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select, WebDriverWait
# from selenium.webdriver.support import expected_conditions
# from selenium.webdriver.common.by import By

from book_app.models import Product

from ..webscraper import DoujinShop


class Melonbooks(DoujinShop):
    def _CheckOpened(self):
        # タイトルに'メロンブックス'が含まれていることを確認する。
        assert 'メロンブックス' in self.driver.title
        try:
            if 'ご指定のページはございません。' in self.driver.find_element_by_css_selector('body > div.box-warning-01 > p').text:
                raise 'page not found'
        except NoSuchElementException:
            pass
            
    def _GetShopNumber(self):
        return Product.MELONBOOKS

    def _GetTitle(self):
        return self.driver.find_element_by_css_selector('h1.str').text

    def _GetCircle(self):
        return self.driver.find_element_by_css_selector('a.circle').text
        
    def _GetAuthor(self):
        # ページ下部の表の要素を取得
        # return self.driver.find_element_by_xpath('//*[@id="description"]/table/tbody/tr[3]/td/a').text
        elements = self.driver.find_elements_by_css_selector('tr.odd')
        # 要素の中から著者のリンクが付いた著者名を探す
        for element in elements:
            # print(element.get_attribute("innerHTML"))
            # 要素から著者のみ残す
            infos = re.findall(r'<a href=.*text_type=author">(.*)</a>', element.get_attribute("innerHTML"))
            # 著者のみ残った要素を検索
            for info in infos:
                if info != None:
                    # 文字列が残っていれば著者
                    return info
                else:
                    # 文字列が残っていないと著者ではない
                    return ''

    def _GetImageUrl(self):
        return self.driver.find_element_by_class_name('tag_sample1').get_attribute("href")

    def _GetImagePath(self, image_url):
        filename = re.findall(r'https://.*image=(.*\.jpg)', image_url)
        return "melonbooks/" + filename[0]

    def _GetLoginUrl(self):
        return 'https://www.melonbooks.co.jp/mypage/history.php'

    def _GetProductListUrl(self):
        return 'https://www.melonbooks.co.jp/mypage/history.php'

    def _MakeLogin(self, user_name, password):
        # ユーザー名とパスワードを入力
        self.driver.find_element_by_id("melonbooks_login_id").send_keys(user_name)
        self.driver.find_element_by_id("melonbooks_password").send_keys(password)
        # ログインボタンクリック
        self.driver.find_element_by_css_selector('#login_mypage > table > tbody > tr:nth-child(2) > td > div > input:nth-child(2)').click()

    def _CheckLogin(self):
        try:
            page_title_element = self.driver.find_element_by_css_selector("#container > div > div.clm_g > div > div.headline.head_l.mb20 > div > h1")
            print(page_title_element.text)
        except NoSuchElementException:
            print('Fail: Melonbooks')
            raise 'Fail: _CheckLogin'

    def _GetProductElements(self):
        # 注文時期:すべて を選択
        Select(self.driver.find_element_by_name('search_select')).select_by_value('999')

        # GO をクリック
        self.driver.find_element_by_css_selector('#form1 > div > div > div > div.clm.clm_r > span.input_btn.br_5 > a').click()
    
        
        while True:
            # エレメント一覧を取得
            product_elements = self.driver.find_elements_by_class_name('product')

            # 次へ ボタンを押す処理
            try:
                # 次へと書いてあるボタンを探す
                elements = self.driver.find_elements_by_class_name('next')
                for element in elements:
                    if '次へ' == element.get_attribute('title'):
                        # 見つけたら次のページへ
                        print(element.get_attribute("title"))
                        element.click()
                        # クリック後に待機
                        time.sleep(5)
                        # driver.implicitly_wait(3)
                        # WebDriverWait(driver, 15).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, 'product')))
                        break
                else:
                    # 次のページは無い
                    print('no more next button')
                    # whileを抜ける
                    break
            except TimeoutException:
                # ロードがタイムアウトした
                # スクリーンショットを撮る。
                self.driver.save_screenshot('error_page_screenshot.png')
                print('Fail: Melonbooks')
                raise 'Fail: _GetProductElements: TimeoutException'
                # break

            
        return product_elements

    def _GetUrlFromProductElement(self, element):
        inner_html = element.get_attribute("innerHTML")
        infos = re.findall(r'<p class="name"><a href="(/detail/detail.php\?product_id=\d+)" title="商品番号:\d+ .*">商品番号:\d+<br>(.*)</a></p>', inner_html)
        return 'https://www.melonbooks.co.jp' + infos[0][0]

