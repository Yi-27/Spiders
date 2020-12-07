import scrapy


class StockspiderSpider(scrapy.Spider):
    name = 'stockspider'
    allowed_domains = ['push2his.eastmoney.com/api/qt/stock/trends2/get?']
    start_urls = ['http://push2his.eastmoney.com/api/qt/stock/trends2/get?/']

    def parse(self, response):
        pass
