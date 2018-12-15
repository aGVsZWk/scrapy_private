from gevent.pool import Pool as BasePool
from gevent.monkey import patch_all
patch_all()

class Pool(BasePool):

    def apply_async(self, func, args=(), kwds={}, callback=None, error_callback=None):
        return super(Pool, self).apply_async(func, args=args, kwds=kwds, callback=callback)

    def close(self):
        pass
