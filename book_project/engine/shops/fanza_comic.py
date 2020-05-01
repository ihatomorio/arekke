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
        assert 'FANZA電子書籍' in self.driver.title or 'DMM電子書籍' in self.driver.title

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
        return self._GetProductListUrl()

    def _GetProductListUrl(self):
        return 'https://book.dmm.co.jp/library/?age_limit=all&expired=0'

    def _MakeLogin(self, user_name, password):
        # open login page
        self.driver.get(self._GetLoginUrl())
        # imput login info
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
        assert '電子書籍' in self.driver.find_element_by_css_selector("div.m-boxMyLibraryPageTitle__txt > span").text

    def _CreateFromProductList(self):
        series_url_list = []

        # 購入済みの本一覧ページを探索
        while(True):
            # 単行本の検索
            try:
                self._AddBookUrlFromProductList()
            except NoSuchElementException:
                pass

            # シリーズ本の検索
            try:
                series_book_elements = self.driver.find_elements_by_css_selector('a.m-boxListBookProductBlock__btn__series')
                for element in series_book_elements:
                    series_url = element.get_attribute('href')
                    series_url_list.append(series_url)
            except NoSuchElementException:
                pass

            # 次のページへ移動
            try:
                self._ClickNextPagingButton()
            except NoSuchElementException:
                # button not found means no more pages
                break

        # シリーズ物のURL一覧から内容を取得する処理
        for series_url in series_url_list:
            print('finding at:', series_url)
            self.driver.get(series_url)

            # 購入済みを探索
            while(True):
                # 単行本の検索
                try:
                    self._AddBookUrlFromProductList()
                except NoSuchElementException:
                    pass

                # 次のページへ移動
                try:
                    self._ClickNextPagingButton()
                except NoSuchElementException:
                    # button not found means no more pages
                    break

    def _AddBookUrlFromProductList(self):
        indivisual_book_elements = self.driver.find_elements_by_css_selector('a.m-boxListBookProductBlock__btn__read')
        for element in indivisual_book_elements:
            if 'アプリで読む' == element.text:
                appli_url = element.get_attribute('href')
                if 'digital_book' in appli_url:
                    product_id = re.findall(r'product_id=([a-z0-9]*)&shop=digital_book', appli_url)
                    book_url = 'https://book.dmm.co.jp/detail/' + product_id[0] + '/'
                    print('found:', book_url)
                    self._QueueCreateProduct(book_url)
                else:
                    product_id = re.findall(r'product_id=([a-z0-9]*)&shop=digital_gbook', appli_url)
                    book_url = 'https://book.dmm.com/detail/' + product_id[0] + '/'
                    print('found:', book_url)
                    self._QueueCreateProduct(book_url)

    def _ClickNextPagingButton(self):
        # ページ遷移ボタン検索
        paging_elements = self.driver.find_elements_by_css_selector('a.m-boxPaging')
        for paging_element in paging_elements:
            # ボタンが＞ならクリック
            if '＞' in paging_element.text:
                paging_element.click()
                break
        else: # button not found means no more pages
            raise NoSuchElementException
