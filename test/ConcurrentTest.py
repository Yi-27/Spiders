# -*- coding: utf-8 -*-

import time
from concurrent.futures import ThreadPoolExecutor

# 可回调的task
def pub_task(msg):
  time.sleep(3)
  return msg

# 创建一个线程池
pool = ThreadPoolExecutor(max_workers=3)

# 往线程池加入2个task
task1 = pool.submit(pub_task, 'a')
task2 = pool.submit(pub_task, 'b')

print(task1.done())  # False done是用来判断任务可完成吗
time.sleep(4)
print(task2.done())  # True

print(task1.result())  # a
print(task2.result())  # b