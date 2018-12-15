import pickle
# pickle功能: 对象与二进制字符串之间的转换
class T(object):
    def __init__(self):
        self.name = "python16"

if __name__ == '__main__':
    obj = T()
    print(obj)
    # # 将对象转换成一个bytes类型的字符串
    result = pickle.dumps(obj)
    print(result)
    with open("temp","wb") as f:
        f.write(result)

    oobj = pickle.loads(result)
    print(oobj.name)

    with open("temp","rb") as f:
        ooobj = f.read()
    print(pickle.loads(ooobj))