# -*- coding: utf-8 -*-

from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
import requests

URLS = ['http://www.csdn.cn', 'http://qq.com', 'http://www.leasonlove.cn']

def task(url, timeout=1):
  return requests.get(url, timeout=timeout)

with ThreadPoolExecutor(max_workers=3) as executor:
  future_tasks = [executor.submit(task, url) for url in URLS]

  for f in future_tasks:
    if f.running():
      print('%s is running' % str(f))

  for f in as_completed(future_tasks):
    try:
      ret = f.done()
      if ret:
        f_ret = f.result()
        print('%s, done, result: %s, %s' % (str(f), f_ret.url, f_ret.content))
    except Exception as e:
      # 第一个url无响应
      f.cancel()
      print(str(e))
