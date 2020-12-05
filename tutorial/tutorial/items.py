# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item, Field


# 自定义实体类
class ProxyItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 这个实体的两个属性
    ip = Field()
    port = Field()
    scheme = Field()  # http/https
    # time = Field()

class TutorialItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


# 东方财富股票当前的信息
class StockItem(Item):
    f2 = Field()  # f2 最新价
    f3 = Field()  # f3 涨跌幅 %
    f4 = Field()  # f4 涨跌额
    f5 = Field()  # f5 成交量（手）
    f6 = Field()  # f6 成交额（元）
    f7 = Field()  # f7 振幅 %
    f8 = Field()  # f8 换手率 %
    f9 = Field()  # f9 市盈率
    f10 = Field()  # f10 量比
    f11 = Field()  # f11 五分钟涨跌
    f12 = Field()  # f12 代码
    f14 = Field()  # f14 名称
    f15 = Field()  # f15 最高价
    f16 = Field()  # f16 最低价
    f17 = Field()  # f17 今开
    f18 = Field()  # f18 昨收
    f20 = Field()  # f20 总市值
    f21 = Field()  # f21 流通市值
    f22 = Field()  # f22 涨速 %
    f23 = Field()  # f23 市净率
    f24 = Field()  # f24 60日涨跌幅
    f25 = Field()  # f25 年初至今涨跌幅 %
    f26 = Field()  # f26 上市时间
    