"""
项目目录,对框架进行测试
"""
from scrapy_plus.core.engine import Engine
# from .spider import BaiduSpider


if __name__ == '__main__':

    engine = Engine()
    engine.start_engine()
