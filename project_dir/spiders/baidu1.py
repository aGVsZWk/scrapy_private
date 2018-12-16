import time
from scrapy_plus.core.spider import Spider
from scrapy_plus.http.request import Request

class BaiduSpider1(Spider):
    name = 'baidu1'
    start_urls = ['https://www.baidu.com']
    total = 0

    # 测试重复请求不被过滤
    def parse(self, response):
        self.total += 1
        time.sleep(2)
        if self.total >10:
            return
        yield Request('https://news.sina.com.cn/roll/#pageid=153&lid=2509&k=&num=50&page=1',filter=False, parse='parse')

    # 测试循环爬取
    # def parse(self, response):
    #     while True:
    #         # 解析数据
    #         print("成功获取响应,准备下一轮")
    #         time.sleep(2)
    #         yield Request("https://news.sina.com.cn/roll/#pageid=153&lid=2509&k=&num=50&page=1",filter=False, parse='parse')