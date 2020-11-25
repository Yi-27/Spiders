import scrapy


class DongfangcaijingSpider(scrapy.Spider):
    name = 'Dongfangcaijing'
    allowed_domains = ['quote.eastmoney.com']
    start_urls = ['http://quote.eastmoney.com/']

    def parse(self, response):
        pass
