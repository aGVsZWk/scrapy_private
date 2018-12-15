"""
根据请求对象(Request)，发起HTTP、HTTPS网络请求，拿到HTTP、HTTPS响应，构建响应对象(Response)并返回
"""
import requests
from scrapy_plus.http.response import Response
from scrapy_plus.utils.log import logger
class Downloader(object):

    def get_response(self,request):
        # 判断请求方法
        if request.method.upper() == "GET":
            response = requests.get(
                url=request.url,
                headers=request.headers,
                cookies=request.cookies,
                params=request.params,
            )
        elif request.method.upper() == "POST":
            response=request.post(
                url=request.url,
                headers=request.headers,
                cookies=request.cookies,
                params=request.params,
                data=request.data
            )
        else:
            raise Exception('框架不支持的请求类型 {}'.format(request.method))

        logger.info("下载器成功获取<{}>对应的响应".format(request.url))

        # 构建响应对象
        res = Response(
            url=response.url,
            body=response.content,
            headers=response.headers,
            code=response.status_code,
            request=request,
            meta=request.meta
        )
        return res