from scrapy_plus import Spider


class BaiduSpider(Spider):
    name = "baidu"
    start_urls = ["http://www.baidu.com","http://www.163.com", 'https://www.baidu.com/s?wd=python&ie=utf-8', 'https://www.baidu.com/s?ie=utf-8&wd=python', "http://www.baidu.com"]

