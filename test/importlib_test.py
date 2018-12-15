# 动态导入模块
import importlib

# 导入一个模块, 根据模块路径
mymodule = importlib.import_module("spiders.baidu")
print(mymodule)
print(dir(mymodule))

# 获取爬虫类
cls = getattr(mymodule,"BaiduSpider")
print(cls)
obj = cls()
print(obj.start_urls)

