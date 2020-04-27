import book_project.engine.webscraper


# url = 'https://booth.pm/ja/items/813108' #マステ
# url = 'https://booth.pm/ja/items/1759716'
url = 'https://booth.pm/ja/items/1393407'
# url = 'https://www.dmm.co.jp/dc/doujin/-/detail/=/cid=d_aoi0538/'
# url = 'https://www.dlsite.com/maniax/work/=/product_id/RJ278847.html'
# url = 'https://www.melonbooks.co.jp/detail/detail.php?product_id=633353
# url = 'https://book.dmm.co.jp/detail/b158aakn00788/' #COMIC LO 2019年11月号

webscraper.get_product_info(url)