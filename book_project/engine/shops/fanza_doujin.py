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
        return self.driver.find_element_by_css_selector('#doujinLIst > div.l-areaMainColumn > div.l-areaProductTitle > div.m-productHeader > div > div > div.m-productInfo > div > div > div > div > h1').text

    def _GetCircle(self):
        return self.driver.find_element_by_xpath('//*[@id="doujinLIst"]/div[2]/div[1]/div[2]/div/div[1]/div/div/div/a').text

    def _GetAuthor(self):
        pass

    def _GetImageUrl(self):
        return self.driver.find_element_by_xpath('//*[@id="fn-slides"]/li[1]/a/img').get_attribute("src")

    def _GetImagePath(self, image_url):
        filename = re.findall(r'https://.*/(.*\.jpg)', image_url)
        return "fanza_doujin/" + filename[0]

    def _GetLoginUrl(self):
        return 'https://login.dlsite.com/login'
    
    def _GetProductListUrl(self):
        return 'https://www.dmm.co.jp/dc/-/mylibrary/'

    def _MakeLogin(self, user_name, password):
        # 商品画面を開く
        self.driver.get(self._GetProductListUrl())

        self.driver.find_element_by_name("login_id").send_keys(user_name)
        self.driver.find_element_by_name("password").send_keys(password)
        self.driver.find_element_by_css_selector('#loginbutton_script_on > span').click()

        # 自動リダイレクト待ちをする
        wait = WebDriverWait(self.driver, 10)
        wait.until(lambda driver: driver.current_url == "https://www.dmm.co.jp/dc/-/mylibrary/")

    def _CheckLogin(self):
        try:
            page_title_element = self.driver.find_element_by_css_selector("#mylibrary-app > div > div:nth-child(1) > div.localListArea12vtK > div.headerTitleList1LTRN > h1")
            print(page_title_element.text)
        except NoSuchElementException:
            print('Fail: FanzaDoujin')
            raise 'Fail: _CheckLogin'

    def _GetProductElements(self):
        return self.driver.find_elements_by_class_name('localListProduct1pSCw')

    def _GetUrlFromProductElement(self, element):
        inner_html = element.get_attribute("innerHTML")
        infos = re.findall(r'<a href=\"/dc/-/mylibrary/detail/=/product_id=(.*/)\".*<p>(.*)</p></div><p', inner_html)
        return 'https://www.dmm.co.jp/dc/doujin/-/detail/=/cid=' + infos[0][0]
