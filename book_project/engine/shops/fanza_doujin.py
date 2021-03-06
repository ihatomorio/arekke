import re

from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException

from book_app.models import Product

from ..webscraper import DoujinShop


class FanzaDoujin(DoujinShop):
    def _CheckOpened(self):
        # タイトルに'FANZA同人'が含まれていることを確認する。
        assert 'FANZA同人' in self.driver.title

    def _GetShopNumber(self):
        return Product.FANZA_DOUJIN

    def _GetTitle(self):
        return self._SupressDiscount(self.driver.find_element_by_css_selector('h1.productTitle__txt').text)

    def _GetCircle(self):
        return self.driver.find_element_by_css_selector('a.circleName__txt').text

    def _GetAuthor(self):
        pass

    def _GetImageUrl(self):
        return self.driver.find_element_by_xpath('//*[@id="fn-slides"]/li[1]/a/img').get_attribute("src")

    def _GetImagePath(self, image_url):
        filename = re.findall(r'https://.*/(.*\.jpg)', image_url)
        return "fanza_doujin/" + filename[0]

    def _GetLoginUrl(self):
        return self._GetProductListUrl()

    def _GetProductListUrl(self):
        return 'https://www.dmm.co.jp/dc/-/mylibrary/'

    def _MakeLogin(self, user_name, password):
        # ログイン画面を開く
        self.driver.get(self._GetLoginUrl())

        self.driver.find_element_by_name("login_id").send_keys(user_name)
        self.driver.find_element_by_name("password").send_keys(password)
        self.driver.find_element_by_css_selector('#loginbutton_script_on > span').click()

        # 自動リダイレクト待ちをする
        wait = WebDriverWait(self.driver, 10)
        wait.until(lambda driver: driver.current_url == "https://www.dmm.co.jp/dc/-/mylibrary/")

    def _CheckLogin(self):
        assert '購入済み作品' in self.driver.find_element_by_css_selector("#mylibrary-app > div > div:nth-child(1) > div.localListArea12vtK > div.headerTitleList1LTRN > h1").text

    def _CreateFromProductList(self):
        for element in self.driver.find_elements_by_class_name('localListProduct1pSCw'):
            inner_html = element.get_attribute("innerHTML")
            infos = re.findall(r'<a href=\"/dc/-/mylibrary/detail/=/product_id=(.*/)\".*<p>(.*)</p></div><p', inner_html)
            self._QueueCreateProduct('https://www.dmm.co.jp/dc/doujin/-/detail/=/cid=' + infos[0][0])