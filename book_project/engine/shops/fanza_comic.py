import re
import time

from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from book_app.models import Product

from ..webscraper import DoujinShop


class FanzaComic(DoujinShop):
    def _CheckOpened(self):
        # ページが無い場合はタイトルが変化(エラーが発生しました)するため先に処理
        # ページが無いことを検知する
        try:
            if '有効なコンテンツを見つけることができませんでした。' in self.driver.find_element_by_css_selector('#w > div > div').text:
                raise self.NoSuchProductPageException
            else:
                # 仮でこの例外を投げる
                raise NoSuchElementException
        except NoSuchElementException:
            pass

        # タイトルに'FANZA電子書籍'が含まれていることを確認する。
        assert 'FANZA電子書籍' in self.driver.title

    def _GetShopNumber(self):
        return Product.FANZA_COMIC

    def _GetTitle(self):
        return self._SupressSuffixedBracket(self.driver.find_element_by_css_selector('#title').text)

    def _GetCircle(self):
        list_title_elements = self.driver.find_elements_by_css_selector('dt.m-boxDetailProductInfo__list__ttl')
        list_detail_elements = self.driver.find_elements_by_css_selector('dd.m-boxDetailProductInfo__list__description')
        
        return self._GetDetailFromTable(list_title_elements, list_detail_elements, '出版社')

    def _GetAuthor(self):
        elements = self.driver.find_elements_by_css_selector("ul.m-boxDetailProductInfoMainList__description__list")
        return elements[0].text

    def _GetImageUrl(self):
        return self.driver.find_element_by_class_name("m-imgDetailProductPack").get_attribute("src")

    def _GetImagePath(self, image_url):
        filename = re.findall(r'https://.*/(.*\.jpg)', image_url)
        return "fanza_comic/" + filename[0]

    def _GetLoginUrl(self):
        return 'https://book.dmm.co.jp/library/?age_limit=all&expired=0'

    def _GetProductListUrl(self):
        return 'https://book.dmm.co.jp/library/?age_limit=all&expired=0'

    def _MakeLogin(self, user_name, password):
        # 商品画面を開く
        self.driver.get(self._GetProductListUrl())

        self.driver.find_element_by_name("login_id").send_keys(user_name)
        self.driver.find_element_by_name("password").send_keys(password)
        self.driver.find_element_by_css_selector('#loginbutton_script_on > span').click()

        # 自動リダイレクト待ちをする
        wait = WebDriverWait(self.driver, 10)
        try:
            wait.until(lambda driver: self.driver.current_url == self._GetProductListUrl())
        except TimeoutException:
            print("redirect timeout: ", self.driver.current_url)
            raise "redirect timeout"

    def _CheckLogin(self):
        try:
            page_title_element = self.driver.find_element_by_css_selector("div.m-boxMyLibraryPageTitle__txt")
            print(page_title_element.text)
        except NoSuchElementException:
            print('Fail: FanzaDoujin')
            raise 'Fail: _CheckLogin'

    def _GetProductUrlList(self):
        url_list = []

        while(True):
            # 単行本の検索
            try:
                indivisual_book_elements = self.driver.find_elements_by_css_selector('a.m-boxListBookProductBlock__btn__read')
                for element in indivisual_book_elements:
                    if 'アプリで読む' == element.text:
                        appli_url = element.get_attribute('href')
                        product_id = re.findall(r'product_id=([a-z0-9]*)&shop=digital_book', appli_url)
                        if product_id:
                            book_url = 'https://book.dmm.co.jp/detail/' + product_id[0] + '/'
                            print(book_url)
                            url_list.append(book_url)
            except NoSuchElementException:
                pass

            # シリーズ本の検索
            try:
                series_book_elements = self.driver.find_elements_by_css_selector('a.m-boxListBookProductBlock__btn__series')
                for element in series_book_elements:
                    series_url = element.get_attribute('href')
                    print(series_url)
                    # not implemented

            except NoSuchElementException:
                pass

            # 次のページへ移動
            try:
                paging_elements = self.driver.find_elements_by_css_selector('a.m-boxPaging')
                for paging_element in paging_elements:
                    if '＞' in paging_element.text:
                        paging_element.click()
                        time.sleep(5)
                        break
                else: # not breaked
                    return url_list
            except NoSuchElementException:
                return url_list

        # not reach
        return url_list

        # シリーズの場合 a.m-boxListBookProductBlock__btn__series