"""
item类
存储数据,写入就不能被修改
"""
class Item(object):
    def __init__(self,data):
        self._data = data

    # 以后就只能调data去看,不能修改
    @property
    def data(self):
        return self._data

