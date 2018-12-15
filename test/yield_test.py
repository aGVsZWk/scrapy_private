import time

n = 0
def foo():
    global n
    my_list = [1,2,3,4,5,6,7]
    for num in my_list:
        time.sleep(1)
        n += 1
        yield num


what = foo()
for it in what:
    print(it)
print(n)

