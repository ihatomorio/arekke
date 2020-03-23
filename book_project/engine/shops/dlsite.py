import re

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select

from book_app.models import Product

from ..webscraper import DoujinShop

class DLSite(DoujinShop):
    def _CheckOpened(self):
        # タイトルに'DLsite'が含まれていることを確認する。
        assert 'DLsite' in self.driver.title

    def _GetShopNumber(self):
        return Product.DLSITE

    def _GetTitle(self):
        self.driver.implicitly_wait(5)
        return self.driver.find_element_by_xpath('//*[@id="work_name"]/a').text

    def _GetCircle(self):
        return self.driver.find_element_by_xpath('//*[@id="work_maker"]/tbody/tr/td/span/a').text

    def _GetAuthor(self):
        pass

    def _GetImageUrl(self):
        return self.driver.find_element_by_xpath("/html/body/div[3]/div[4]/div[1]/div/div[1]/div[1]/div/div/div[2]/div/div[1]/div[1]/ul/li[1]/img").get_attribute("src")

    def _GetImagePath(self, image_url):
        filename = re.findall(r'https://.*/(RJ.*_img_main\.jpg)', image_url)
        return "dlsite/" + filename[0]
    
    def _GetLoginUrl(self):
        return 'https://login.dlsite.com/login'
    
    def _GetProductListUrl(self):
        return 'https://www.dlsite.com/maniax/mypage/userbuy/complete'

    def _MakeLogin(self, user_name, password):
        self.driver.find_element_by_name("login_id").send_keys(user_name)
        self.driver.find_element_by_name("password").send_keys(password)
        self.driver.find_element_by_css_selector('body > div.l-container > div > div > section > div.mainBox-body > div.contentBox > div:nth-child(1) > div > form > div.loginBtn > button').click()

    def _CheckLogin(self):
        # 一覧ページを開く
        self.driver.get(self._GetProductListUrl())
        assert '購入履歴' in self.driver.find_element_by_css_selector("h1").text

    def _GetProductElements(self):
        # 一覧ページを開く
        # self.driver.get(self._GetProductListUrl())
        
        # 18歳以上です
        try:
            self.driver.find_element_by_css_selector('body > div.adult_check_box._adultcheck > div > ul > li.btn_yes.btn-approval > a').click()
        except NoSuchElementException:
            pass

        # クーポンを閉じる
        try:
            self.driver.find_element_by_class_name('fs16').click()
            
            # 一覧ページに戻る
            self.driver.get(self._GetProductListUrl())
        except NoSuchElementException:
            pass

        # 購入月:すべて を選択
        Select(self.driver.find_element_by_id('_start')).select_by_value('all')

        # 並び順: 古い順を選択
        Select(self.driver.find_element_by_name('sort')).select_by_value('2')

        # 表示 をクリック
        self.driver.find_element_by_id('_display').click()

        return self.driver.find_elements_by_class_name('work_name')

    def _GetUrlFromProductElement(self, element):
        inner_html = element.get_attribute("innerHTML")
        infos = re.findall(r' +<a href="(http.*\.html)">(.*)</a>', inner_html)
        return infos[0][0]

