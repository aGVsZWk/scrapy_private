from scrapy_plus.conf import settings
# 协程池尽可能放所有模块之前, 里面打猴子补丁会替换掉后面阻塞的模块
if settings.ASYNC_TYPE == "thread":
    from multiprocessing.dummy import Pool
elif settings.ASYNC_TYPE == "coroutine":
    # from gevent.pool import Pool
    # 名字不能用async, 关键字, 用了会报错
    from scrapy_plus.async_.coroutine import Pool  # 导入协程池对象
    pass
else:
    raise Exception("框架不支持的并发类型{}".format(settings.ASYNC_TYPE))


from .downloader import Downloader
from .scheduler import Scheduler

from scrapy_plus.http.request import Request
from scrapy_plus.item import Item



from datetime import datetime
import time
from scrapy_plus.utils.log import logger

import importlib


from scrapy_plus.conf.settings import SCHEDULER_PERSIST
from scrapy_plus.utils.status_collector import NormalStatsCollector,ReidsStatsCollector

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
        # self.scheduler = Scheduler()
        self.downloader = Downloader()
        self.pipelines = pipelines

        self.spider_mids = spider_mids
        self.downloader_mids = downloader_mids

        # 设置计数器
        # self.total_request_num = 0
        # self.total_response_num = 0
        # 根据配置使用单机的状态收集器或者分布式的状态收集器
        if SCHEDULER_PERSIST:
            self.collector = ReidsStatsCollector()
        else:
            self.collector = NormalStatsCollector()

        self.scheduler = Scheduler(self.collector)


        # 创建线程池
        self.pool = Pool()
        self.is_running = True

    def start_engine(self):
        start = datetime.now()
        logger.info("框架启动的时间为:[{}]".format(start))
        logger.info("并发类型为{}".format(settings.ASYNC_TYPE))
        logger.info("并发数量为{}".format(settings.MAX_ASYNC_THREAD_NUMBER))

        self._start_engine()
        stop = datetime.now()
        logger.info("框架停止的时间为:[{}]".format(stop))
        logger.info("框架运行的时间为:[{}]".format((stop-start).total_seconds()))
        self.collector.clear()    # 清除redis中所有的计数的值,但不清除指纹集合; 视情况而看

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
                # self.total_request_num += 1
                self.collector.incr(self.collector.request_nums_key)

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
        # print(">>>>>",parse)

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

                # self.total_request_num += 1
                self.collector.incr(self.collector.request_nums_key)


            elif isinstance(result, Item):
                # 8.如果结果为item对象,调用管道的process_item方法处理item数据

                # ----5.调用爬虫中间件的process_item方法获取起始的请求
                for spider_mid in self.spider_mids:
                    result = spider_mid.process_item(result)

                for pipeline in self.pipelines:

                    result = pipeline.process_item(result,spider)


            else:
                raise Exception("不支持的解析结果{}".format(result))

        # self.total_response_num += 1
        self.collector.incr(self.collector.response_nums_key)


    def _callback(self,temp):
        if self.is_running:
            self.pool.apply_async(self._excute_request_response_item, callback=self._callback)

    def _errorback(self,exception):
        try:
            raise exception
        except Exception as e:
            logger.exception(e)



    def _start_engine(self):

        self.pool.apply_async(self._start_requests, error_callback=self._errorback)

        for i in range(settings.MAX_ASYNC_THREAD_NUMBER):
            self.pool.apply_async(self._excute_request_response_item,callback=self._callback,error_callback=self._errorback)

        while True:
            time.sleep(0.0000000001)
            # print(self.total_request_num,self.total_response_num,self.scheduler.repeat_request_num)
            # time.sleep(1)
            if self.collector.request_nums !=0:
                if self.collector.request_nums == self.collector.response_nums + self.collector.repeat_request_nums:
                    self.is_running = False
                    break

        self.pool.close()  # 协程池无close方法
        self.pool.join()


