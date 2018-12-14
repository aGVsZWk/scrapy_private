"""
构建请求信息(初始的)，也就是生成请求对象(Request)
解析响应对象，返回数据对象(Item)或者新的请求对象(Request)
"""
from scrapy_plus.http.request import Request
from scrapy_plus.item import Item
class Spider():

    start_url = "http://www.baidu.com"

    def start_requests(self):
        return Request(self.start_url)

    def parse(self,response):
        return Item(response.url)

