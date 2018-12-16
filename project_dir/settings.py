DEFAULT_LOG_FILENAME = 'mysettings.log'    # 默认日志文件名称

# 增加以下信息：
# 启用的爬虫类
SPIDERS = [
    # 'spiders.baidu.BaiduSpider',
    # 'spiders.douban.DoubanSpider',
    'spiders.baidu1.BaiduSpider1',

]

# 启用的管道类
PIPELINES = [
    # 'pipelines.BaiduPipeline',
    # 'pipelines.DoubanPipeline'
]

# 启用的爬虫中间件类
SPIDER_MIDDLEWARES = [
    # 'middlewares.TestSpiderMiddleware1',
    # 'middlewares.TestSpiderMiddleware2'
]

# 启用的下载器中间件类
DOWNLOADER_MIDDLEWARES = [
    # 'middlewares.TestDownloaderMiddleware1',
    # 'middlewares.TestDownloaderMiddleware2'
]

ASYNC_TYPE = 'coroutine'

# 设置调度器的内容是否要持久化
# 量个值：True和False
# 如果是True，那么就是使用分布式，同时也是基于请求的增量式爬虫
# 如果是False, 不使用redis队列，会使用python的set存储指纹和请求
# True: 持久化, 使用分布式, 断点和ctrl+c也ok,自动保存 , 实现了断点续爬
SCHEDULER_PERSIST = True

REDIS_HOST = '192.168.188.134'

REDIS_DB = 15

# 是否清除指纹集合
FP_PERSIST = False