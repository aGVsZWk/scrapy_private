"""
项目目录,对框架进行测试
"""
from scrapy_plus.core.engine import Engine
# from .spider import BaiduSpider
from spiders.baidu import BaiduSpider
from spiders.douban import DoubanSpider


if __name__ == '__main__':
    baidu = BaiduSpider()
    douban = DoubanSpider()
    # spiders = [baidu,douban]
    spiders = {"baidu":baidu,"douban":douban}
    engine = Engine(spiders)
    engine.start_engine()
