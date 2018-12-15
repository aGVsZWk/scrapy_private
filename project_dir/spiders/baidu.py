from scrapy_plus.core.spider import Spider
from scrapy_plus.http.request import Request
from scrapy_plus.item import Item


class BaiduSpider(Spider):
    start_urls = ["http://www.baidu.com","http://www.163.com"]

