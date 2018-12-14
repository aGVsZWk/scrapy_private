from .downloader import Downloader
from .scheduler import Scheduler
from .spider import Spider
from scrapy_plus.http.request import Request
from scrapy_plus.item import Item
from .pipeline import Pipeline

class Engine(object):

    def __init__(self):
        self.spider = Spider()
        self.scheduler = Scheduler()
        self.downloader = Downloader()
        self.pipeline = Pipeline()

    def start_engine(self):
        self._start_engine()

    def _start_engine(self):
        # 1.调用spider模块的start_request方法获取起始的请求
        start_request = self.spider.start_requests()

        # 2.调用调度器模块的put_request方法将请求放入调度器的待爬取队列
        self.scheduler.put_request(start_request)

        # 3.调用调度器模块的get_request方法将请求从调度器拿出来
        request = self.scheduler.get_request()

        # 4.调用downloader模块的get_response方法,获取响应
        response = self.downloader.get_response(request)

        # 5.调用spider的parse方法解析响应,获得返回的结果
        result = self.spider.parse(response)

        # 6.判断结果是何种类型的数据
        if isinstance(result,Request):
            # 7.如果结果为请求对象,调用调度器模块的put_request方法将请求放入调度器的待爬取队列
            self.scheduler.put_request(result)
        elif isinstance(result,Item):
            # 8.如果结果为item对象,调用管道的process_item方法处理item数据
            self.pipeline.process_item(result)
        else:
            raise Exception("不支持的解析结果{}".format(result))

