# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from scrapy.exceptions import DropItem  # 一个丢弃的异常
from itemadapter import ItemAdapter  # 用于包裹Item，不直接操作Item
import json

class TutorialPipeline:
    def process_item(self, item, spider):
        return item


# 自定义proxy实体对象处理管道
class ProxyPipeline(object):
    
    def __init__(self):
        self.proxy_set = set()  # 去重集合，写在这里
    
    def open_spider(self, spider):
        """打开爬虫时做的事"""

        self.file = open("proxy_json.json", "a")
        # 写日志
        spider.logger.info("A jsonFile open")
        
    def close_spder(self, spider):
        """关闭爬虫时做的事"""
        self.file.close() # 关闭写文件
        # 写日志
        spider.logger.info("A jsonFile closed")
        
    def process_item(self, item, spider):
        """处理每个实体项目"""
        adapter_item = ItemAdapter(item)  # 不直接操作项目
        
        # 判断ip是否已存在集合中
        if adapter_item.get("ip") in self.proxy_set:
            raise DropItem("该ip已经存在，不重复存！")
        
        self.proxy_set.add(item)
        # 写进文件
        line = json.dumps(adapter_item.asdict()) + "\n"
        self.file.write(line)
        return item  # 返回该项目
    