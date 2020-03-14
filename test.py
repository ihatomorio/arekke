
class ProductInfo(models.Product):
    def UpdateProductInfo(self):
        # ブラウザーを起動
        options = Options()
        options.binary_location = '/opt/google/chrome-beta/google-chrome-beta'
        options.add_argument('--headless')
        options.add_argument('--no-sandbox') #rootに必要
        driver = webdriver.Chrome(options=options)
        print('look')
        print(self.url)

        # Webページにアクセス
        driver.get(self.url)

        # 商品名をアップデート
        self.title = self.GetProductTitleFromDriver(driver)

        # サークル名をアップデート
        self.circle = self.GetProductTitleFromDriver(driver)

        # 著者を取得
        self.author = self.GetProductAuthorFromDriver(driver)

        # 画像URLを取得
        image_url = self.GetProductImageUrlFromDriver(driver)

        # 画像のファイル名を取得
        filename = self.GetImageFilenameFromUrl(image_url)

        # 保存用パスを生成 MEDIA_ROOT = '/root/repos/websq/book_project/media'
        path = self.CreateSavePath(filename)

        # 画像を保存用パスへダウンロード
        urllib.request.urlretrieve(image_url, path)

        # shop番号を更新
        self.shop = GetShopNumber()

        # ブラウザを閉じる
        webscraper.close_browser(driver)

    def GetProductTitleFromDriver(self, driver):
        raise 'Called abstract method'

    def GetProductCircleFromDriver(self, driver):
        raise 'Called abstract method'

    def GetProductAuthorFromDriver(self, driver):
        raise 'Called abstract method'

    def GetProductImageUrlFromDriver(self, driver):
        raise 'Called abstract method'

    def GetImageFilenameFromUrl(self, url):
        raise 'Called abstract method'

    def CreateSavePath(self, filename):
        raise 'Called abstract method'

    def GetShopNumber(self):
        raise 'Called abstract method'