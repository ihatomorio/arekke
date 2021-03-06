from abc import ABCMeta, abstractmethod
from concurrent import futures
import re
import sys

import chromedriver_binary
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
import urllib.request

from django.conf import settings
from django.utils import timezone

from book_app.models import Account, Product


# global variable
_executor = futures.ThreadPoolExecutor(max_workers=4)


class DoujinShop(metaclass=ABCMeta):

    def __init__(self):
        self.driver = None
        self.request_by = None

    @staticmethod
    def UpdateProductInfo(product, set_shop_num):
        from .shops.booth import Booth
        from .shops.dlsite import DLSite
        from .shops.fanza_comic import FanzaComic
        from .shops.fanza_doujin import FanzaDoujin
        from .shops.melonbooks import Melonbooks
        # サイト別に取得する インスタンスの作成
        if 'booth.pm' in product.url:
            doujinshop = Booth()
        elif 'www.dlsite.com' in product.url:
            doujinshop = DLSite()
        elif 'book.dmm.co.jp' in product.url or 'book.dmm.com' in product.url:
            doujinshop = FanzaComic()
        elif 'www.dmm.co.jp/dc/doujin' in product.url:
            doujinshop = FanzaDoujin()
        elif 'www.melonbooks.co.jp' in product.url:
            doujinshop = Melonbooks()
        else:
            product.title = '未対応URL'
            product.save()
            return

        # 店の番号をセット
        if set_shop_num:
            product.shop = doujinshop._GetShopNumber()

        # 取得処理を実行
        try:
            doujinshop.__UpdateProductInfoFromUrl(product, product.url)

        # 商品が無い場合
        except DoujinShop.NoSuchProductPageException:
            # loadingまたは取得失敗の場合のみ更新
            if( product.title == 'loading' or product.title == '取得失敗' ):
                product.title = '商品ページなし'

        # その他の例外
        except Exception as exception:
            product.title = '取得失敗'
            print('exception: ', exception, file=sys.stderr)
            doujinshop.driver.save_screenshot('error.png')
            import traceback
            traceback.print_exc()

        # 取得結果の保存
        product.save()

    @staticmethod
    def GetProductList(account, request_by):
        # from .shops.booth import Booth
        from .shops.dlsite import DLSite
        from .shops.fanza_comic import FanzaComic
        from .shops.fanza_doujin import FanzaDoujin
        from .shops.melonbooks import Melonbooks

        # shop属性でインスタンスを切り替え
        if account.shop == Account.DLSITE:
            doujinshop = DLSite()
        elif account.shop == Account.FANZA_COMIC:
            doujinshop = FanzaComic()
        elif account.shop == Account.FANZA_DOUJIN:
            doujinshop = FanzaDoujin()
        elif account.shop == Account.MELONBOOKS:
            doujinshop = Melonbooks()
        else:
            return

        # インスタンスに対して商品一覧取得を開始
        try:
            doujinshop.__GetProductList(account, request_by)
        except Exception as exception:
            print('exception: ', exception, file=sys.stderr)
            doujinshop.driver.save_screenshot('error.png')
            import traceback
            traceback.print_exc()

        # 取得完了の時間を入れる
        account.date = timezone.now()
        account.save()

    @staticmethod
    def CreateFromUrl(url, request_by, set_shop_num=True, title=None, circle=None, bought_date=None):
        # URL被りがあったら生成中断
        if Product.objects.filter(owner=request_by, url=url):
            return

        # 商品を生成
        product = Product.objects.create(
            title = 'loading',
            owner = request_by,
            shop = 0,
            url = url
        )

        # 並列処理で商品情報を取得する
        try:
            instance = DoujinShop.UpdateProductInfo(product, set_shop_num)
        except Exception as exception:
            print('exception: ', exception, file=sys.stderr)
            instance.driver.save_screenshot('error.png')
            import traceback
            traceback.print_exc()

        if product.title == '商品ページなし':
            product.title = title
            product.circle = circle

        product.bought_date = bought_date

        product.save()

    def __UpdateProductInfoFromUrl(self, product, url):
        print('Update: ', url)
        # ブラウザを開く
        self.__OpenBrowser()
        self.driver.get(url)

        # ページのタイトルを確認する
        self._CheckOpened()

        # 商品名を取得
        product.title = self._GetTitle()

        try:
            # ショップ名称を取得
            product.circle = self._GetCircle()
        except NoSuchElementException:
            product.circle = ''

        try:
            # 作家名を取得
            product.author = self._GetAuthor()
        except NoSuchElementException:
            product.author = ''

        try:
            # 画像を取得
            image_url = self._GetImageUrl()
            if image_url != None:
                product.image_path = self.__GetImage(image_url)
        except NoSuchElementException:
            product.image_url = ''

        # ブラウザを閉じる
        self.__CloseBrowser()

    def __GetProductList(self, account, request_by):
        self.request_by = request_by

        # ブラウザを生成
        self.__OpenBrowser()

        # ログインする
        print('making login')
        self._MakeLogin(account.user, account.password)

        # ログインを確認
        print('checking login')
        self._CheckLogin()
        print('login succeeded')

        # 商品URL一覧を取得し商品を作成
        print('getting product')
        self._CreateFromProductList()
        print('getting product end')

        # ブラウザを閉じる
        self.__CloseBrowser()

    def _QueueCreateProduct(self, url, title=None, circle=None, bought_date=None):
        print('Queued:', url)
        assert self.request_by != None
        _executor.submit(fn=DoujinShop.CreateFromUrl, url=url, request_by=self.request_by, title=title, circle=circle, bought_date=bought_date)

    # ブラウザの生成
    def __OpenBrowser(self, url=None):
        options = Options()
        options.binary_location = '/usr/bin/google-chrome'
        options.add_argument('--headless')
        options.add_argument('--no-sandbox') #rootに必要
        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(30)
        if url != None:
            self.driver.get(url)

    # ブラウザ終了
    def __CloseBrowser(self):
        self.driver.quit()

    @abstractmethod
    def _CheckOpened(self):
        pass

    @abstractmethod
    def _GetShopNumber(self):
        pass

    @abstractmethod
    def _GetTitle(self):
        pass

    @abstractmethod
    def _GetCircle(self):
        pass

    @abstractmethod
    def _GetAuthor(self):
        pass

    def __GetImage(self, image_url):
        # 保存用パスを生成
        image_path = self._GetImagePath(image_url)

        # 画像をダウンロード
        save_path = self.__GetSavePath(image_path)
        self.__DownloadImage(image_url, save_path)

        # 画像の保存パスを返す
        return image_path

    @abstractmethod
    def _GetImageUrl(self):
        pass

    @abstractmethod
    def _GetImagePath(self, image_url):
        pass

    def __GetSavePath(self, image_path):
        # settings.MEDIA_ROOT = '/root/repos/websq/book_project/media'
        return settings.MEDIA_ROOT + '/' + image_path

    def __DownloadImage(self, image_url, save_path):
        urllib.request.urlretrieve(image_url, save_path)

    @abstractmethod
    def _GetLoginUrl(self):
        pass

    @abstractmethod
    def _GetProductListUrl(self):
        pass

    @abstractmethod
    def _MakeLogin(self, user_name, password):
        pass

    @abstractmethod
    def _CheckLogin(self):
        pass

    @abstractmethod
    def _CreateFromProductList(self):
        pass

    class NoSuchProductPageException(Exception):
        pass

    def _SupressDiscount(self, text):
        # 正規表現を試みる
        matched = re.findall(r'(【\d\d[%％](OFF|還元)】)+ *(.*)', text)
        if len(matched) == 0:
            # マッチ文字列なし
            return text
        else:
            # マッチの最終パターンのみ返す
            return matched[0][len(matched[0])-1]

    def _SupressSuffixedBracket(self, text):
        # 正規表現を試みる
        matched = re.findall(r'(.*?)(【.*】)+$', text)
        if len(matched) == 0:
            # マッチ文字列なし
            return text
        else:
            # マッチの先頭パターンのみ返す
            return matched[0][0]

    def _GetDetailFromTable(self, title_elements, detail_elements, requirement):
        # title_elementsについて入っているものチェックし、requirementのときその内容を返す
        for title_element, detail_element in zip(title_elements, detail_elements):
            if title_element.text == requirement:
                return detail_element.text
        else:
            return None