import re

import xml.etree.ElementTree as ET

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
        name_type = self.driver.find_element_by_xpath('//*[@id="work_maker"]/tbody/tr/th').text
        if( name_type == 'サークル名' ):
            # 同人誌
            circle_name = self.driver.find_element_by_xpath('//*[@id="work_maker"]/tbody/tr/td/span/a').text
            return circle_name
        else:
            # コミック
            auth_company = self.driver.find_element_by_xpath('//*[@id="work_maker"]/tbody/tr[2]/td/span/a').text
            return auth_company

    def _GetAuthor(self):
        # 同人誌
        column_title = self.driver.find_element_by_xpath('//*[@id="work_outline"]/tbody/tr[2]/th').text
        if( column_title == '作者'):
            return self.driver.find_element_by_xpath('//*[@id="work_outline"]/tbody/tr[2]/td').text

        # コミック
        column_title = self.driver.find_element_by_xpath('//*[@id="work_maker"]/tbody/tr[1]/th').text
        if( column_title == '著者'):
            return self.driver.find_element_by_xpath('//*[@id="work_maker"]/tbody/tr[1]/td').text

        return None

        # author_html = self.driver.find_element_by_id('work_right_name').get_attribute('innerHTML')
        # # parse as xml
        # root = ET.fromstring(author_html)
        # # find author row
        # for tag_tr in root.iter('tr'):
        #     # find author column at row
        #     for child in tag_tr.iter('th'):
        #         # if author, return inner text
        #         if( child.text == '著者'):
        #             return tag_tr.find('./td/a').text

    def _GetImageUrl(self):
        image_html = self.driver.find_element_by_css_selector('li.slider_item.active').get_attribute("innerHTML")
        image_url = re.findall(r'(img.dlsite.jp/modpub/images2/work/.*_img_main\.jpg)', image_html)
        return 'https://' + image_url[0]

    def _GetImagePath(self, image_url):
        filename = re.findall(r'https://.*/([RB]J.*_img_main\.jpg)', image_url)
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

    def _GetProductUrlList(self):
        url_list = []

        # 18歳以上です
        try:
            self.driver.find_element_by_css_selector('body > div.adult_check_box._adultcheck > div > ul > li.btn_yes.btn-approval > a').click()
        except NoSuchElementException:
            pass

        # クーポンを閉じる
        try:
            self.driver.find_element_by_class_name('fs16').click()
        except NoSuchElementException:
            pass

        # 今月の購入履歴を取得
        self.driver.get('https://www.dlsite.com/home/mypage/userbuy')

        for element in self.driver.find_elements_by_class_name('work_name'):
            inner_html = element.get_attribute("innerHTML")
            infos = re.findall(r' +<a href="(http.*\.html)">(.*)</a>', inner_html)
            url_list.append(infos[0][0])

        # 過去の購入履歴を取得
        self.driver.get(self._GetProductListUrl())

        # 購入月:すべて を選択
        Select(self.driver.find_element_by_id('_start')).select_by_value('all')

        # 表示 をクリック
        self.driver.find_element_by_id('_display').click()

        for element in self.driver.find_elements_by_class_name('work_name'):
            inner_html = element.get_attribute("innerHTML")
            infos = re.findall(r' +<a href="(http.*\.html)">(.*)</a>', inner_html)
            url_list.append(infos[0][0])

        # コミック:すべて を選択
        Select(self.driver.find_element_by_id('_type')).select_by_value('14')

        # 表示 をクリック
        self.driver.find_element_by_id('_display').click()

        for element in self.driver.find_elements_by_class_name('work_1col'):
            inner_html = element.get_attribute("innerHTML")
            infos = re.findall(r' +<a href="(https://www.dlsite.com/books/work/=/product_id/.*\.html)">.*</a>', inner_html)
            for product_url in infos:
                url_list.append(product_url)

        return url_list
