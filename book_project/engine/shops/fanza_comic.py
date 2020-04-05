import re

from book_app.models import Product

from ..webscraper import DoujinShop


class FanzaComic(DoujinShop):
    def _CheckOpened(self):
        # タイトルに'FANZA電子書籍'が含まれていることを確認する。
        assert 'FANZA電子書籍' in self.driver.title

    def _GetShopNumber(self):
        return Product.FANZA_COMIC

    def _GetTitle(self):
        return self.driver.find_element_by_css_selector('#title').text

    def _GetCircle(self):
        pass

    def _GetAuthor(self):
        return self.driver.driver.find_element_by_class_name("m-boxDetailProductInfoMainList__description__list").text

    def _GetImageUrl(self):
        return self.driver.find_element_by_class_name("m-imgDetailProductPack").get_attribute("src")

    def _GetImagePath(self, image_url):
        filename = re.findall(r'https://.*/(.*\.jpg)', image_url)
        return "fanza_comic/" + filename[0]
