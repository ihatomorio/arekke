import re

from book_app.models import Product

from ..webscraper import DoujinShop


class Booth(DoujinShop):
    def _CheckOpened(self):
        # タイトルに'BOOTH'が含まれていることを確認する。
        assert 'BOOTH' in self.driver.title

    def _GetShopNumber(self):
        return Product.BOOTH

    def _GetTitle(self):
        return self.driver.find_element_by_css_selector("h2.u-tpg-title1").text

    def _GetCircle(self):
        return self.driver.find_element_by_css_selector("div.u-text-ellipsis").text

    def _GetAuthor(self):
        pass

    def _GetImageUrl(self):
        return self.driver.find_element_by_css_selector('body > div.page-wrap > main > div.market-item-detail.u-bg-white > article > div > div.u-bg-white.u-pt-600.u-px-700 > div.container > div > div.u-order-0.l-col-3of5.u-pr-500 > div.primary-image-area.slick-initialized.slick-slider > div > div > div.slick-slide.slick-current.slick-active > div > div > div > img').get_attribute("src")

    def _GetImagePath(self, image_url):
        filename = re.findall(r'https://.*/(.*_base_resized\.jpg)', image_url)
        return "booth/" + filename[0]

    def _GetLoginUrl(self):
        pass

    def _GetProductListUrl(self):
        pass

    def _MakeLogin(self, user_name, password):
        pass

    def _CheckLogin(self):
        pass

    def _GetProductUrlList(self):
        pass
