import scrapy
import json

class TestrandomproxyspiderSpider(scrapy.Spider):
    name = 'TestRandomProxySpider'
    # allowed_domains = ['abc.com']
    # start_urls = ['http://abc.com/']

    def start_requests(self):
        for _ in range(50):
            yield scrapy.Request('http://httpbin.org/ip', dont_filter=True)
            yield scrapy.Request('https://httpbin.org/ip', dont_filter=True)

    def parse(self, response, **kwargs):
        print(json.loads(response.text))
