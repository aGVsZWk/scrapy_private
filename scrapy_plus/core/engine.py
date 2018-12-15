from .downloader import Downloader
from .scheduler import Scheduler

from scrapy_plus.http.request import Request
from scrapy_plus.item import Item



from datetime import datetime
import time
from scrapy_plus.utils.log import logger


from scrapy_plus.conf import settings
import importlib

from multiprocessing.dummy import Pool

def auto_import(path, spider=False):

    if spider:
        obj_list = {}
    else:
        obj_list = []
    for data in path:
        module_name = data[:data.rfind('.')]
        cls_name = data[data.rfind('.') + 1:]

        # 动态加载模块
        mod = importlib.import_module(module_name)

        # 从模块中获取类
        cls = getattr(mod, cls_name)

        # 实例化一个对象
        obj = cls()
        if spider:
            obj_list[obj.name] = obj
        else:
            obj_list.append(obj)

    return obj_list

spiders = auto_import(settings.SPIDERS, spider=True)
pipelines = auto_import(settings.PIPELINES)
spider_mids = auto_import(settings.SPIDER_MIDDLEWARES)
downloader_mids = auto_import(settings.DOWNLOADER_MIDDLEWARES)



class Engine(object):

    def __init__(self):
        self.spiders = spiders
        self.scheduler = Scheduler()
        self.downloader = Downloader()
        self.pipelines = pipelines

        self.spider_mids = spider_mids
        self.downloader_mids = downloader_mids

        # 设置计数器
        self.total_request_num = 0
        self.total_response_num = 0

        # 创建线程池
        self.pool = Pool()

    def start_engine(self):
        start = datetime.now()
        logger.info("框架启动的时间为:[{}]".format(start))
        self._start_engine()
        stop = datetime.now()
        logger.info("框架停止的时间为:[{}]".format(stop))
        logger.info("框架运行的时间为:[{}]".format((stop-start).total_seconds()))


    def _start_requests(self):

        # 遍历爬虫列表, 分别获取每一个爬虫
        for spider_name, spider in self.spiders.items():

            # 1.调用spider模块的start_request方法获取起始的请求
            start_requests = spider.start_requests()

            for start_request in start_requests:
                # ----1.调用爬虫中间件的process_request方法获取起始的请求
                for spider_mid in self.spider_mids:
                    start_request = spider_mid.process_request(start_request)

                # 给请求添加对应爬虫名
                start_request.spider_name = spider_name

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
        for downloader_mid in self.downloader_mids:
            request = downloader_mid.process_request(request)

        # 4.调用downloader模块的get_response方法,获取响应
        response = self.downloader.get_response(request)

        # ----3.调用下载器中间件的process_response方法处理响应
        for downloader_mid in self.downloader_mids:
            response = downloader_mid.process_response(response)

        # 动态获取爬虫
        spider = self.spiders[request.spider_name]

        parse = getattr(spider, request.parse)
        # 5.调用spider的parse方法解析响应,获得返回的结果
        results = parse(response)


        for result in results:

            # 6.判断结果是何种类型的数据
            if isinstance(result, Request):
                # 7.如果结果为请求对象,调用调度器模块的put_request方法将请求放入调度器的待爬取队列

                # ----4.调用爬虫中间件的process_request方法获取起始的请求
                for spider_mid in self.spider_mids:
                    result = spider_mid.process_request(result)

                # 为请求对象添加spider_name
                result.spider_name = request.spider_name

                self.scheduler.put_request(result)

                # 对解析出来的请求做累加

                self.total_request_num += 1

            elif isinstance(result, Item):
                # 8.如果结果为item对象,调用管道的process_item方法处理item数据

                # ----5.调用爬虫中间件的process_item方法获取起始的请求
                for spider_mid in self.spider_mids:
                    result = spider_mid.process_item(result)

                for pipeline in self.pipelines:

                    result = pipeline.process_item(result,spider)


            else:
                raise Exception("不支持的解析结果{}".format(result))

        self.total_response_num += 1

    def _callback(self,temp):
        self.pool.apply_async(self._excute_request_response_item, callback=self._callback)

    def _start_engine(self):

        self.pool.apply_async(self._start_requests)

        for i in range(settings.MAX_ASYNC_THREAD_NUMBER):
            self.pool.apply_async(self._excute_request_response_item,callback=self._callback)

        while True:

            # print(self.total_request_num,self.total_response_num,self.scheduler.repeat_request_num)
            # time.sleep(1)
            if self.total_request_num !=0:
                if self.total_request_num == self.total_response_num + self.scheduler.repeat_request_num:
                    break


