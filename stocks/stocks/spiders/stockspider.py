import scrapy
from scrapy.utils.project import get_project_settings # 导入配置文件
import json
import time
import pandas as pd
import threading
from datetime import datetime
from ..utils import SeleniumUtils, DBUtils, KafkaUtils
import os
from scrapy_redis.spiders import RedisSpider

class StockspiderSpider(RedisSpider):  # 继承redisSpider而不是scrapy.Spider
    name = 'stockspider'
    # allowed_domains = ['push2his.eastmoney.com/api/qt/stock/trends2/get?']
    # start_urls = ['http://push2his.eastmoney.com/api/qt/stock/trends2/get?/']
    # redis_batch_size =
    # redis_encoding =
    redis_key = "stocksURL"  # 派发任务的redis
    
    def __init__(self):
        """初始化
        获取scrapy配置的对象
        selenium的driver
        获取redis连接

        """
        super(StockspiderSpider, self).__init__()
    
        # 获取配置对象
        self.settings = get_project_settings()  # 获取配置对象
    
        # 获取selenium的无窗口driver，用于之后登陆得到cookies
        # self.driver = SeleniumUtils.get_selenium()
    
        self.mysql = DBUtils.get_mysql()
    
        # 获取redis连接，用于存取cookies
        self.redis = DBUtils.get_redis()
    
        # 获取mongoDB连接，用于存储所有数据
        self.mongo = DBUtils.get_mongo()
    
        # 获取Kafka工具类对象
        self.kafka = KafkaUtils()
    
        # 获取一个同步生产者，用于记录当前爬虫的运行日志
        # self.loggerProducer = self.kafka.get_sync_producer("StocksLog_%s" % round(time.time()))
    
        # 行情股票列表。即行情中心，用于构造请求URL
        with open("center.json", "r", encoding="utf-8") as f:
            self.__params_list = json.load(f)
    
        # 返回字段对应的中文名，比如f2: 最新价。用于最终保存成文件
        with open("filed_name.json", "r", encoding="utf-8") as f:
            self.__filed_name = json.load(f)
           
    def close(self, spider):
        """关闭各种资源"""
        # self.driver.close()
        self.mysql.close()
        self.redis.close()
        self.mongo.close()
        
    def parse(self, response, **kwargs):
        """其实到这里就已经是爬取到对应股票的页面了，只需要对其进行处理就行了
        数据是个列表
        # 日期  时间           ？ 现价   最高价  最低价 成交量 成交金额 成交金额/成交量
        ['2020-12-07 09:15,19.30, 19.30, 19.30, 19.30, 0,     0.00,      19.300',
         '2020-12-07 09:16,19.29, 19.30, 19.30, 19.29, 0,     0.00,      19.300',
         '2020-12-07 09:17,19.30, 19.30, 19.30, 19.30, 0,     0.00,      19.300',
         ...
        ]
        """
        res = response.text
        data_json = res[res.find("(") + 1:-2]  # 截取字符串，方便从json字符串转换成字典
        data_dict = json.loads(data_json)
        stock_name = data_dict["data"]["name"]
        stock_id = data_dict["data"]["code"]

        # data_dict["data"]["time"]  1607585643  最后更新时间
        # 但是保存时只要保存每天的数据就行
        # 如果当天数据正在每分钟不停的更新，就覆盖掉之前的数据，或者往里追加数据就行
        stock_time = datetime.fromtimestamp(data_dict["data"]["time"]).strftime("%Y%m%d")

        data = data_dict["data"]["trends"]  # 是个列表

        # mongoDB直接存 全部文档，数据库名：股票名，表名为每天时间（只精确到日）

        # 使用多线程加速读取
        t1 = threading.Thread(target=self.mysql_save, args=(data, self.mysql))
        t2 = threading.Thread(target=self.kafka_save, args=(data, self.kafka, stock_name, stock_time))

        tlist = [t1, t2]
        for t in tlist:
            t.start()
        for t in tlist:
            t.join()  # 必须要这样，防止主线程执行完后，就关闭连接了！

    def mysql_save(self, data, mysql):
        """
        先判断是否存在股票对应的存储表
            不存在即创建
            存在就开始插入数据
                这里要将时间设为每行数据的时间索引（用于去重）
        """
        cursor = mysql.cursor()
    
        # 添加结束释放游标
        cursor.close()

    def kafka_save(self, data, kafka, stock_name, spider_time):
        # 获取到一个异步生产者，用于存爬取到的数据
        producer = kafka.get_producer(stock_name)  # 比如 shangzheng
        data_dict = {"time": spider_time, "data": data}
        producer.produce(json.dumps(data_dict).encode())