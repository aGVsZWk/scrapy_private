"""
项目目录,对框架进行测试
"""
from scrapy_plus.core.engine import Engine
# from .spider import BaiduSpider
from spiders.baidu import BaiduSpider
from spiders.douban import DoubanSpider
from pipelines import BaiduPipeline,DoubanPipeline
from middlewares import TestSpiderMiddleware1,TestSpiderMiddleware2,TestDownloaderMiddleware1,TestDownloaderMiddleware2


if __name__ == '__main__':
    baidu = BaiduSpider()
    douban = DoubanSpider()
    # spiders = [baidu,douban]
    spiders = {baidu.name:baidu,douban.name:douban}

    # 实例化管道对象
    pipelines = [BaiduPipeline(),DoubanPipeline()]

    # 实例化中间件对象
    spider_mids = [TestSpiderMiddleware1(),TestSpiderMiddleware2()]

    downloader_mids = [TestDownloaderMiddleware1(),TestDownloaderMiddleware2()]

    engine = Engine(spiders, pipelines, spider_mids, downloader_mids)
    engine.start_engine()
