import scrapy
from scrapy.utils.project import get_project_settings # 导入配置文件
import json
import time
import pandas as pd
from datetime import datetime
from ..utils import SeleniumUtils, DBUtils, KafkaUtils

class OneStockSpider(scrapy.Spider):
    name = 'onestock'
    allowed_domains = ['push2his.eastmoney.com/api/qt/stock/trends2/get?']
    start_urls = ['http://push2his.eastmoney.com/api/qt/stock/trends2/get?/']

    def __init__(self):
        """
        初始化
        获取redis、Mongo连接等
        """
        super(OneStockSpider, self).__init__()
        
        self.settings = get_project_settings()  # 获取配置对象
        self.redis = DBUtils.get_redis()
        self.mongo = DBUtils.get_mongo()
        self.kafka = KafkaUtils()

    def close(self, spider):
        """关闭各种资源"""
        # self.driver.close()
        self.redis.close()
        self.mongo.close()
        
        
    def start_requests(self):
        # 设置headers
        headers = {
            "Host": "push2his.eastmoney.com",
            "Connection": "keep-alive",
            "Referer": "http://quote.eastmoney.com/",
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        }

        # 公共的请求参数
        public_params = [
            "ut=7eea3edcaed734bea9cbfc24409ed989",
            "ndays=1",
            "iscr=1",  # 也算上9点30前的十五分钟，即从9点15开始
            # "secid=0.000001",  # 股票代码 小于600000为0.，大于为1.
            "fields1=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13",  # 这些只起到辅助作用
            "fields2=f51,f52,f53,f54,f55,f56,f57,f58"  # 这些才是关键
        ]
        
        # 从Kafka中取出股票代码，构造URL
        stock_consumer = self.kafka.get_simple_consumer("stockCode")
        for message in stock_consumer:
            if message is not None:
                # print(stock.offset, stock.value.decode())
                stock = message.value.decode()
                if stock["code"] < 600000:
                    public_params.append("secid=0.%s"%stock["code"])
                else:
                    public_params.append("secid=1.%s"%stock["code"])
                
                cb = "cb=jQuery1124009071583642216097_%s" % str(time.time()).replace(".", "")[:-4]
                timestamp = "_=%s" % str(time.time()).replace(".", "")[:-4]
                
                url = "http://push2his.eastmoney.com/api/qt/stock/trends2/get?%s&%s&%s" % (
                    cb, '&'.join(public_params), timestamp
                )
                
                # 每个股票的简介
                meta = {
                    "_type": "%s_%s_%s" % (stock["name"], stock["code"], datetime.now().strftime("%Y%m%d%H%M"))
                }

                yield scrapy.Request(url, headers=headers, callback=self.stock_parse, meta=meta,
                                     dont_filter=False)  # 只爬一次

                # 当全爬完时就终止循环，不然会一直卡在着
                if (message.offset == message.latest_available_offsets()[0][0][0] - 1):
                    break
        
        
        
    def parse(self, response, **kwargs):
        pass
