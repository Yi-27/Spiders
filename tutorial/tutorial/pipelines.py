# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from scrapy.exceptions import DropItem  # 一个丢弃的异常
from itemadapter import ItemAdapter  # 用于包裹Item，不直接操作Item
import json
from datetime import datetime
from scrapy.utils.project import get_project_settings # 导入配置文件
import pymongo
from redis import StrictRedis, ConnectionPool



class TutorialPipeline:
    def process_item(self, item, spider):
        return item


# 自定义proxy实体对象处理管道
class ProxyPipeline(object):
    
    def __init__(self):
        self.proxy_set = set()  # 去重集合，写在这里
    
    def open_spider(self, spider):
        """打开爬虫时做的事"""
        self.file = open("proxy_josn.json", "a")
        # 写日志
        spider.logger.info("打开JSON文件准备写入！")
        
    def close_spider(self, spider):
        """关闭爬虫时做的事"""
        self.file.close() # 关闭写文件
        # 写日志
        spider.logger.info("写入完毕关闭JSON文件！")
        
    def process_item(self, item, spider):
        """处理每个实体项目"""
        adapter_item = ItemAdapter(item)  # 不直接操作项目
        
        # 判断ip是否已存在集合中
        if adapter_item.get("ip") in self.proxy_set:
            raise DropItem("该ip已经存在，不重复存！")
        
        self.proxy_set.add(item)
        # 写进文件
        line = json.dumps(adapter_item.asdict()) + ",\n"
        self.file.write(line)
        return item  # 返回该项目
    
    
# 写入MongoDB的模板管道
class MongoDBPipeline(object):
    
    def __init__(self):
        self.settings = get_project_settings()  # 获取配置对象
        self.client = None  # 数据库连接
        self.db = None  # 数据库
        self.hqzx_doc = None  # 行情中心
        self.doc_buffer = []  # 用于insert_many一次性添加
        self.time_format = "%Y-%m-%d %H:%M:%S"  # 时间格式化
    
    def open_spider(self, spider):  # 注意，spider可以用来判断是哪个爬虫的管道
        if spider.name == "hangqingzhongxin":
            # 获取配置信息
            host = self.settings.get("MONGODB_HOST", default="127.0.0.1")
            port = self.settings.get("MONGODB_PORT", default=27017)
            db = self.settings.get("MONGODB_DBNAME", default="dfcf")
            doc = self.settings.get("MONGODB_DOCNAME", default="")
            
            # 获取数据库连接、数据库、文档
            self.client = pymongo.MongoClient(host=host, port=port)
            self.db = self.client[db]
            self.hqzx_doc = self.db[doc]  # 行情中心
            
            # 写日志
            spider.logger.info("连接MongoDB成功！ %s" % datetime.now().strftime(self.time_format))

    def close_spider(self, spider):
        if spider.name == "hangqingzhongxin":
            # 关闭数据库连接
            self.client.close()
            
            # 写日志
            spider.logger.info("关闭MongoDB成功！ %s" % datetime.now().strftime(self.time_format))

            
    def process_item(self, item, spider):
        """处理每个实体项"""
        if spider.name == "hangqingzhongxin":
            adapter_item = ItemAdapter(item)  # 不直接操作实体项目
            
            # 插入到MongoDB对应的文档里
            self.hqzx_doc.insert_one(adapter_item.asdict())
            # 当然可以攒上许多个文档后用insert_many一次性添加进去，这样更好
            if self.doc_buffer.__len__() >= 50:
                try:
                    self.hqzx_doc.insert_many(self.doc_buffer)
                except Exception as e:
                    print(e)
                    self.doc_buffer.append(adapter_item.asdict())  # 如果写入失败就
                else:
                    # 先写日志
                    spider.logger.info("已将文档缓冲区中的文档放入数据库中！ %s"%datetime.now().strftime(self.time_format))
                    self.doc_buffer.clear()  # 若try没抛异常就说明成功添加进数据库中，清理掉缓冲区
            else:
                self.doc_buffer.append(adapter_item.asdict())


# 写入MongoDB的模板管道
class RedisPipeline(object):
    
    def __init__(self):
        self.settings = get_project_settings()  # 获取配置对象
        self.pool = None  # 数据库连接池
        self.redis = None  # 数据库连接
        self.kv_buffer = {}  # 用于mset一次性添加
        self.time_format = "%Y-%m-%d %H:%M:%S"  # 时间格式化
    
    def open_spider(self, spider):  # 注意，spider可以用来判断是哪个爬虫的管道
        if spider.name == "":
            # 获取配置信息
            host = self.settings.get("REDIS_HOST", default="127.0.0.1")
            port = self.settings.get("REDIS_PORT", default=6379)
            
            # 获取数据库连接池、数据库
            self.pool = ConnectionPool(host=host, port=port)  # db默认为0，用户名和密码默认无
            self.redis = StrictRedis(connection_pool=self.pool)
            
            # 写日志
            spider.logger.info("连接Redis成功！ %s" % datetime.now().strftime(self.time_format))
    
    def close_spider(self, spider):
        if spider.name == "":
            # 关闭数据库连接
            self.redis.close()
            spider.logger.info("关闭Redis成功！ %s" % datetime.now().strftime(self.time_format))
    
    def process_item(self, item, spider):
        """处理每个实体项"""
        if spider.name == "":
            adapter_item = ItemAdapter(item)  # 不直接操作实体项目
            
        