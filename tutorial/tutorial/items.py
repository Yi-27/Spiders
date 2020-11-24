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
    time = Field()

class TutorialItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
