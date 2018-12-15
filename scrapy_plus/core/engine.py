from .downloader import Downloader
from .scheduler import Scheduler
from .spider import Spider
from scrapy_plus.http.request import Request
from scrapy_plus.item import Item
from .pipeline import Pipeline
import time

from scrapy_plus.middlewares.spider_middleware import SpiderMiddleware
from scrapy_plus.middlewares.downloader_middleware import DownloaderMiddleware
from datetime import datetime
from scrapy_plus.utils.log import logger

class Engine(object):

    def __init__(self,spider):
        self.spider = spider
        self.scheduler = Scheduler()
        self.downloader = Downloader()
        self.pipeline = Pipeline()

        self.spider_mid = SpiderMiddleware()
        self.downloader_mid = DownloaderMiddleware()

        # 设置计数器
        self.total_request_num = 0
        self.total_response_num = 0

    def start_engine(self):
        start = datetime.now()
        logger.info("框架启动的时间为:[{}]".format(start))
        self._start_engine()
        stop = datetime.now()
        logger.info("框架停止的时间为:[{}]".format(stop))
        logger.info("框架运行的时间为:[{}]".format((stop-start).total_seconds()))


    def _start_requests(self):
        # 1.调用spider模块的start_request方法获取起始的请求
        start_requests = self.spider.start_requests()

        for start_request in start_requests:
            # ----1.调用爬虫中间件的process_request方法获取起始的请求
            start_request = self.spider_mid.process_request(start_request)

            # 2.调用调度器模块的put_request方法将请求放入调度器的待爬取队列
            self.scheduler.put_request(start_request)

            # 请求计数器加1
            self.total_request_num += 1

    def _excute_request_response_item(self):

        # 3.调用调度器模块的get_request方法将请求从调度器拿出来
        request = self.scheduler.get_request()
        if request is None:
            return

        # ----2.调用下载器中间件的process_request方法处理请求
        request = self.downloader_mid.process_request(request)

        # 4.调用downloader模块的get_response方法,获取响应
        response = self.downloader.get_response(request)

        # ----3.调用下载器中间件的process_response方法处理响应
        response = self.downloader_mid.process_response(response)

        parse = getattr(self.spider, request.parse)
        # 5.调用spider的parse方法解析响应,获得返回的结果
        results = parse(response)


        for result in results:

            # 6.判断结果是何种类型的数据
            if isinstance(result, Request):
                # 7.如果结果为请求对象,调用调度器模块的put_request方法将请求放入调度器的待爬取队列

                # ----4.调用爬虫中间件的process_request方法获取起始的请求
                result = self.spider_mid.process_request(result)

                self.scheduler.put_request(result)

                # 对解析出来的请求做累加

                self.total_request_num += 1

            elif isinstance(result, Item):
                # 8.如果结果为item对象,调用管道的process_item方法处理item数据

                # ----5.调用爬虫中间件的process_item方法获取起始的请求
                result = self.spider_mid.process_item(result)

                self.pipeline.process_item(result)


            else:
                raise Exception("不支持的解析结果{}".format(result))

        self.total_response_num += 1

    def _start_engine(self):

        self._start_requests()

        while True:

            self._excute_request_response_item()

            if self.total_request_num == self.total_response_num:
                break
            # break
















