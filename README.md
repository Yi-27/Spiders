# Spiders
 一些爬虫



# Scrapy



除了在终端运行Scrapy爬虫，还可以在py文件中运行

```python
from scrapy import cmdline
cmdline.execute("scrapy crawl example".split())
```



新版本的Scrapy使用Xpath或CSS选择器已经可以不用**extract()**和**extract_first()**了

改用**get()**和**getall()**，但是旧命令还能用。