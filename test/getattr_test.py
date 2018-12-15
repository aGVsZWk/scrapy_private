class T(object):

    def __init__(self):
        self.name = "python16"
    def func(self):
        print("我被调用了")

# getattr: 通过字符串, 获取方法或属性
t = T()
func = getattr(t,"func")
func()
n = getattr(t,"name")
print(n)