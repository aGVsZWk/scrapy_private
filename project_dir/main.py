"""
项目目录,对框架进行测试
"""
from project_dir.spider import DoubanSpider
from scrapy_plus.core.engine import Engine
# from .spider import BaiduSpider
from spider import BaiduSpider #todo 搞不懂这里为什么scrapy会找到项目目录的spider

if __name__ == '__main__':
    baidu = BaiduSpider()
    douban = DoubanSpider()
    engine = Engine(douban)
    engine.start_engine()
