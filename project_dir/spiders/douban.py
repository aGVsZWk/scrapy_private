from scrapy_plus import Spider
from scrapy_plus.http.request import Request
from scrapy_plus.item import Item



class DoubanSpider(Spider):
    name = "douban"
    start_urls = []  # 重写start_requests方法后，这个属性就没有设置的必要了

    def start_requests(self):
        # 重写start_requests方法，返回多个请求
        base_url = 'http://movie.douban.com/top250?start='
        for i in range(0, 50, 25):    # 逐个返回第1-10页的请求属相
            url = base_url + str(i)
            yield Request(url)

    def parse(self, response):
        '''解析豆瓣电影top250列表页'''
        title_list = []    # 存储所有的
        for li in response.xpath("//ol[@class='grid_view']/li"):    # 遍历每一个li标签
            title = li.xpath(".//span[@class='title'][1]/text()")   # 提取该li标下的 标题
            title_list.append(title[0])
            # title_list.apppend(title[0])    # 故意写错,发现程序卡死,没任何提示

        yield Item(title_list)    # 返回标题
#
# class DoubanSpider(Spider):
#     name = "douban"
#     start_urls = []  # 重写start_requests方法后，这个属性就没有设置的必要了
#
#     def start_requests(self):
#         base_url = 'http://movie.douban.com/top250?start='
#         for i in range(0, 50, 25):    # 逐个返回第1-10页的请求属相
#             url = base_url + str(i)
#             yield Request(url)
#
#     def parse(self, response):
#         '''解析豆瓣电影top250列表页'''
#         for li in response.xpath("//ol[@class='grid_view']/li")[:2]:  # 遍历每一个li标签
#             item = {}
#             item["title"] = li.xpath(".//span[@class='title'][1]/text()")
#
#             detail_url = li.xpath(".//div[@class='info']/div[@class='hd']/a/@href")[0]
#             yield Request(detail_url, parse="parse_detail", meta={"item":item})
#
#     def parse_detail(self, response):
#         '''解析详情页'''
#
#         item = response.meta["item"]
#         item["url"] = response.url
#         # print("item",item)
#         yield Item(item)    # 返回标题
