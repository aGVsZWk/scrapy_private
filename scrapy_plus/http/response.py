"""
响应类
参数:url, headers, body, code, request
code:状态码
"""
from lxml import etree
import json
import re

class Response(object):

    def __init__(self, url, headers, body, code, request, meta):
        self.url = url
        self.headers = headers
        self.body = body
        self.code = code
        self.request = request
        self.meta = meta

    def xpath(self, rule):
        # 创建elements对象
        html = etree.HTML(self.body)
        return html.xpath(rule)

    @property
    def json(self):
        return json.loads(self.body)

    def re_findall(self, rule, data=None):
        if not data:
            data = self.body.decode()
        return re.findall(rule, data, re.S)


