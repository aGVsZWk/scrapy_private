"""
 请求类的定义
 参数: url, headers, cookies, params, data, method
 """
class Request(object):

    def __init__(self, url, headers={}, cookies={}, params={}, data={}, method="GET"):
        self.url = url
        self.headers = headers
        self.cookies = cookies
        self.params = params
        self.data = data
        self.method = method

