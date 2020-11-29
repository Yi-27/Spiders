# -*- coding: utf-8 -*-
# 用来通过py文件来运行爬虫

from scrapy import cmdline

spidername = ""
cmdline.execute(f"scrapy crawl {spidername}")  # 可能还需要导出数据，就相应的加上-o参数

