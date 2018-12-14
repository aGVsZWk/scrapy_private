"""
缓存请求对象(Request)，并为下载器提供请求对象，实现请求的调度：
对请求对象进行去重判断：实现去重方法_filter_request，该方法对内提供，因此设置为私有方法
"""
## py3
# from queue import Queue
## py2
# from Queue import Queue

from six.moves.queue import Queue # six模块会根据py的版本自动切换使用的队列

class Scheduler(object):
    def __init__(self):
        self.queue = Queue()

    def put_request(self,request):
        '''
        将请求放入待爬取队列
        :param request:
        :return:
        '''
        if not self._filter_request(request):
            self.queue.put(request)

    def get_request(self):
        '''
        从待爬取队列中获取一个请求对象
        :return:
        '''
        return self.queue.get()

    def _filter_request(self,request):
        '''
        url在请求队列中返回True,不在返回False
        :param request:
        :return:
        '''
        return False
