"""
构建请求信息(初始的)，也就是生成请求对象(Request)
解析响应对象，返回数据对象(Item)或者新的请求对象(Request)
"""
from scrapy_plus.http.request import Request
from scrapy_plus.item import Item
class Spider():

    start_urls = []

    def start_requests(self):
        for start_url in self.start_urls:
            yield Request(start_url)

    def parse(self,response):
        yield Item(response.url)

