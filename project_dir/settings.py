DEFAULT_LOG_FILENAME = 'mysettings.log'    # 默认日志文件名称

# 增加以下信息：
# 启用的爬虫类
SPIDERS = [
    'spiders.baidu.BaiduSpider',
    'spiders.douban.DoubanSpider'
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

# ASYNC_TYPE = 'coroutine'