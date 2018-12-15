import redis
from scrapy_plus.conf import settings


class BaseFilterContainer(object):

    def add_fp(self, fp):
        '''往去重容器添加一个指纹'''
        pass

    def exists(self, fp):
        '''判断指纹是否在去重容器中'''
        pass

class NoramlFilterContainer(BaseFilterContainer):
    '''利用python的集合类型, 普通过滤器, 用于单机版'''


    def __init__(self):
        self._filter_container = set()

    def add_fp(self, fp):
        ''''''
        self._filter_container.add(fp)

    def exists(self, fp):
        '''判断指纹是否在去重容器中'''
        if fp in self._filter_container:
            return True
        else:
            return False

class RedisFilterContainer(BaseFilterContainer):
    '''利用redis的指纹集合, 分布式版'''
    REDIS_SET_NAME = settings.REDIS_SET_NAME
    REDIS_SET_HOST = settings.REDIS_HOST
    REDIS_SET_PORT = settings.REDIS_PORT
    REDIS_SET_DB = settings.REDIS_DB

    def __init__(self):
        self._redis = redis.StrictRedis(host=self.REDIS_SET_HOST, port=self.REDIS_SET_PORT ,db=self.REDIS_SET_DB)
        self._name = self.REDIS_SET_NAME

    def add_fp(self, fp):
        '''往去重容器添加一个指纹'''
        self._redis.sadd(self._name, fp)

    def exists(self, fp):
        '''判断指纹是否在去重容器中'''
        return self._redis.sismember(self._name, fp) # 存在返回1 不存在返回0