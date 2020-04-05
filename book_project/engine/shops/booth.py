import re

from book_app.models import Product
from selenium.common.exceptions import NoSuchElementException

from ..webscraper import DoujinShop


class Booth(DoujinShop):
    def _CheckOpened(self):
        # タイトルに'BOOTH'が含まれていることを確認する。
        assert 'BOOTH' in self.driver.title

        # 年齢確認を突破
        try:
            if '年齢確認' in self.driver.find_element_by_tag_name("h1").text:
                self.driver.find_element_by_css_selector('a.adult-check-nav').click()
        except NoSuchElementException:
            pass

    def _GetShopNumber(self):
        return Product.BOOTH

    def _GetTitle(self):
        return self.driver.find_element_by_css_selector("h2.u-tpg-title1").text

    def _GetCircle(self):
        return self.driver.find_element_by_css_selector("div.u-text-ellipsis").text

    def _GetAuthor(self):
        return None

    def _GetImageUrl(self):
        return self.driver.find_element_by_css_selector('body > div.page-wrap > main > div.market-item-detail.u-bg-white > article > div > div.u-bg-white.u-pt-600.u-px-700 > div.container > div > div.u-order-0.l-col-3of5.u-pr-500 > div.primary-image-area.slick-initialized.slick-slider > div > div > div.slick-slide.slick-current.slick-active > div > div > div > img').get_attribute("src")

    def _GetImagePath(self, image_url):
        filename = re.findall(r'https://.*/(.*_base_resized\.jpg)', image_url)
        return "booth/" + filename[0]

    def _GetLoginUrl(self):
        raise NotImplementedError

    def _GetProductListUrl(self):
        raise NotImplementedError

    def _MakeLogin(self, user_name, password):
        raise NotImplementedError

    def _CheckLogin(self):
        raise NotImplementedError

    def _GetProductUrlList(self):
        raise NotImplementedError
