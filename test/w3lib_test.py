# 规范化url, 对键排序, 键相同则根据值排序
import w3lib.url

start_urls = [ 'https://www.baidu.com/s?wd=python&ie=utf-8', 'https://www.baidu.com/s?ie=utf-8&wd=python']

for url in start_urls:
    print(w3lib.url.canonicalize_url(url))

