"""
缓存请求对象(Request)，并为下载器提供请求对象，实现请求的调度：
对请求对象进行去重判断：实现去重方法_filter_request，该方法对内提供，因此设置为私有方法
"""
## py3
# from queue import Queue
## py2
# from Queue import Queue
import hashlib

from six.moves.queue import Queue # six模块会根据py的版本自动切换使用的队列
from scrapy_plus.utils.queue import Queue as RedisQueue
from scrapy_plus.utils.set import NoramlFilterContainer,RedisFilterContainer
from scrapy_plus.conf.settings import SCHEDULER_PERSIST

from scrapy_plus.utils.log import logger
import w3lib.url

class Scheduler(object):
    def __init__(self):

        if SCHEDULER_PERSIST:
            self.queue = RedisQueue()
            self._filter_container = RedisFilterContainer()
        else:
            self.queue = Queue()
            self._filter_container = NoramlFilterContainer()

        self.repeat_request_num = 0

    def put_request(self,request):
        '''
        将请求放入待爬取队列
        :param request:
        :return:
        '''
        fp = self._gen_fp(request)
        if not self._filter_request(fp):
            self.queue.put(request)
            self._filter_container.add_fp(fp)
        else:
            self.repeat_request_num += 1
            logger.info("重复的请求<{}>已经被过滤掉了,hash值为<{}>".format(request.url,fp))

    def get_request(self):
        '''
        从待爬取队列中获取一个请求对象
        :return:
        '''
        try:
            return self.queue.get(False)
        except:
            return

    def _filter_request(self,fp):
        '''
        url在请求队列中返回True,不在返回False
        :param request:
        :return:
        '''


        if self._filter_container.exists(fp):
            return True
        else:
            return False

    def _gen_fp(self,request):
        """url请求参数顺序不同的处理"""

        url = w3lib.url.canonicalize_url(request.url)
        method = request.method.upper()
        params = str(sorted(request.params.items()))
        data = str(sorted(request.params.items()))
        hashstr = (url + method + params + data).encode()

        # 创建hash对象
        sha1 = hashlib.sha1()
        # 将字符串更新到对象中
        sha1.update(hashstr)
        # 获取指纹
        fp = sha1.hexdigest()

        return fp
