"""
负责处理数据对象
"""
class Pipelinet(object):

    def process_item(self,item):
        print("当前管道正在处理的数据为({})".format(item.data))