"""
响应类
参数:url, headers, body, code, request
code:状态码
"""

class Response(object):

    def __init__(self, url, headers, body, code, request):
        self.url = url
        self.headers = headers
        self.body = body
        self.code = code
        self.request = request