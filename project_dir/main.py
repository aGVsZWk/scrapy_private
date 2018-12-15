"""
项目目录,对框架进行测试
"""
from scrapy_plus.core.engine import Engine
# from .spider import BaiduSpider
from spiders.baidu import BaiduSpider
from spiders.douban import DoubanSpider
from pipelines import BaiduPipeline,DoubanPipeline

if __name__ == '__main__':
    baidu = BaiduSpider()
    douban = DoubanSpider()
    # spiders = [baidu,douban]
    spiders = {baidu.name:baidu,douban.name:douban}

    # 实例化管道对象
    pipelines = [BaiduPipeline(),DoubanPipeline()]

    engine = Engine(spiders,pipelines)
    engine.start_engine()
