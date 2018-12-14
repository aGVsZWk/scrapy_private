# scrapy_plus/middlewares/downloader_middlewares.py
from scrapy_plus.utils.log import logger

class DownloaderMiddleware(object):
    '''下载器中间件基类'''

    def process_request(self, request):
        '''预处理请求对象'''
        logger.info("这是下载器中间件：process_request方法")
        return request

    def process_response(self, response):
        '''预处理响应对象'''
        logger.info("这是下载器中间件：process_response方法")
        return response