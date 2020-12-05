import scrapy
from scrapy.utils.project import get_project_settings # 导入配置文件
import json
import time
import pandas as pd
from datetime import datetime
from ..utils import SeleniumUtils, DBUtils, KafkaUtils


class DongfangcaifuHQZXSpider(scrapy.Spider):
    name = 'hangqingzhongxin'  # 行情中心的爬虫
    allowed_domains = ['quote.eastmoney.com']
    start_urls = ['http://quote.eastmoney.com/']

    def __init__(self):
        """初始化
        获取scrapy配置的对象
        selenium的driver
        获取redis连接
        
        """
        super(DongfangcaifuHQZXSpider, self).__init__()

        # 获取配置对象
        self.settings = get_project_settings()  # 获取配置对象
        
        # 获取selenium的无窗口driver，用于之后登陆得到cookies
        self.driver = SeleniumUtils.get_selenium()
        
        # 获取redis连接，用于存取cookies
        self.redis = DBUtils.get_redis()
        
        # 获取mongoDB连接，用于存储所有数据
        self.mongo = DBUtils.get_mongo()
        
        # 获取Kafka工具类对象
        self.kafka = KafkaUtils()
        
        # 获取一个同步生产者，用于记录当前爬虫的运行日志
        self.loggerProducer = self.kafka.get_sync_producer("HQZXLog_%s"%round(time.time()))
        
        # 行情股票列表。即行情中心，用于构造请求URL
        with open("center.json", "r", encoding="utf-8") as f:
            self.__params_list = json.load(f)

        # 返回字段对应的中文名，比如f2: 最新价。用于最终保存成文件
        with open("filed_name.json", "r", encoding="utf-8") as f:
            self.__filed_name = json.load(f)
    
    def close(self, spider):
        """关闭各种资源"""
        self.driver.close()
        self.redis.close()
        self.mongo.close()

    def start_requests(self):
    
        # 公共的请求参数
        public_params = [
            "pn=1",  # 页数
            "po=0",  # 0 1 升序
            "np=1",  # 1 1 降序
            "ut=bd1d9ddb04089700cf9c27f6f7426281",
            "fltt=2",
            "invt=2",
            "fid=f12",  # 按代码排序
            "fields=f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f26",
        ]
        for p in self.__params_list:
            cb = "cb=jQuery112404633069651159658_%s" % str(time.time()).replace(".", "")[:-4]
            timestamp = "_=%s" % str(time.time()).replace(".", "")[:-4]
        
            url = "http://69.push2.eastmoney.com/api/qt/clist/get?%s&%s&%s&%s"%(
                cb, '&'.join(public_params), '&'.join(list(p.values())[0]), timestamp
            )
            print(url)
        
            meta = {
                "_type": "%s_%s"%(p.keys()[0], datetime.now().strftime("%Y%m%d%H%M"))  # 表示是哪类请求，比如，是沪深A股，还是上证A股，再配上时间
            }
        
            # headers 和 cookies都在后续的下载中间件中添加了上了
            # 这里只要专注于 构造Request请求 就行
            yield scrapy.Request(url, callback=self.hqzx_parse, meta=meta, dont_filter=False)  # 只爬一次

    def hqzx_parse(self, response, **kwargs):
        """
        用于处理返回的响应
        注意的是，在此之前就已经对响应做过了一些处理
        比如，将响应直接写入kafka中
        这里要做的就是将数据持久化存储到本地
        """
        res = response.text
        data_json = res[res.find("(") + 1:-2]  # 截取字符串，方便从json字符串转换成字典
        data_dict = json.loads(data_json)
        data = data_dict["data"]["diff"]  # 类型是[{},{},...]

        # 直接用pandas转成DataFrame，然后存在本地
        data_pd = pd.DataFrame(data)
        data_pd.rename(columns=self.__filed_name, inplace=True)
        data_pd.to_csv(f"./stocks/{response.meta['_type']}.csv", encoding='GBK', index=False)


    def parse(self, response, **kwargs):
        pass
