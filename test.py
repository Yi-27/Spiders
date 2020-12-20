import threading
import time
import sys

def print(st):
    sys.stdout.write(st+"\n")

class A:pass

num1 = threading.local()
num2 = A()
num1.x = 0
num2.x = 0

def worker(num1,num2):
    num1.x = 0  # 因为local对象是线程安全的，每个线程中的属性都不一样，为了防止属性报错，先赋值
    for i in range(100):
        num1.x += 1
        num2.x += 1
    print("{} 中 num1.x = {},num2.x = {}".format(threading.current_thread(),num1.x,num2.x))

t1 = threading.Thread(target=worker,args=(num1,num2))
t1.start()
t2 = threading.Thread(target=worker,args=(num1,num2))
t2.start()

t1.join()
t2.join()
print("main Thread Exits")
print("num1.x = {},num2.x = {}".format(num1.x,num2.x))
