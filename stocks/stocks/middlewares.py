# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
from fake_useragent import UserAgent
from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
import json
from fake_useragent import UserAgent



"""---------------------------下载中间件-----------------------------"""
# 随机设置UA  下载中间件
class RandomUserAgentMiddleware(object):  # 下载中间件
    
    def __init__(self):
        self.ua = UserAgent()
    
    def process_request(self, request, spider):
        # 设置随机的UA
        request.headers["User-Agent"] = self.ua.random


# 设置单个股票爬虫的headers
# 需要注意该下载中间件的优先级要比随机设置UA的下载中间件要高一点
class HQZXHeadersMiddleware(object):
    
    def process_request(self, request, spider):
        if spider.name == "stockspider":
            # 设置headers
            headers = {
                "Host": "86.push2.eastmoney.com",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
                "Referer": "http://quote.eastmoney.com/",
                "Accept": "*/*",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            }
            request.headers = {**request.headers, **headers}  # 合并两个字典


# 设置cookies
class StocksSetCookiesMiddleware(object):
    
    def process_request(self, request, spider):
        if spider.name == "stockspider":
            redis = spider.redis
            if redis.exists("stocksCookies"):
                # request.cookies = json.loads(redis.get("dfcfCookies").decode())  # 设置cookies
                request.headers['Cookie'] = redis.get("stocksCookies").decode()  # 暂时先这样设置，其实应该是按上面那样设置的
            else:
                cookies = "qgqp_b_id=498c8ab46440318862f8757ff37ca2aa; em-quote-version=topspeed; ct=TsW12_qQdpEM19gtyIzscqRCcsD0XELSxOrVxh5k6fLxeXKzSlnI4X_PWNiAKPsLC6tbNkKsar68KBgD0O04sConpDu_o_SO99iMImwe2fI-OkKdBb_LqkkR4L_-522lbOoOOl2Von2gmPd4u4lzLP4Wb-K2WilpJvtBfW54nOM; ut=FobyicMgeV7bfas_M05TDBOeyCFFs48knKwC5VBjLh4OQceJBUzUsQihFbc8gUi_5OPQwgb3yLNkDoEO-0b-qSRrv6swX_WeiFe1bMQk9dFXwUVQLPPG3AI_grbg8Kj9CS-4nHIh0D7f4atKAtC1Kmm9UwSPBCwGsdrV2HUYNkfPjiQsNg0I4czRn1MDjrZ1gv79YMZPw0XXw9nQ827reuVxG7t8NnVoGT8Uy3NPk_BXeC6g9vH41S4meWl-yP5vRMwxNspw5vfq_zGoP66zm5CiLArZqWrt; pi=6182326063031944%3bg6182326063031944%3b%e6%97%b6%e4%b8%8d%e6%88%91%e5%be%8513%3bElmy3jk86IdbBrEXagIDOw5c2fjFUC8HxzUlggSXDigqDG%2fEfCVdjq4BbKQIVBziKxfVF21JdoEuk0UVewrFPXcFIi8rS5BO438uVbb0nEHjaggvC%2b%2fE%2flNEZ2W46YPWZY9vpYtBkaAKTk9B0hDbllFpOcg%2b5HQQgv3VxSVrLV0gMowrOGrZ0skiZnww2NBbw1ZxF2h4%3bGZAkM%2f3fupUnr0cFGFWL8KUvvlMhaxvjVaDweUiLGy4YNE%2f0hSlRvvjqyu7u0DlRpC%2ffZX3F5VbPu95F0fcx6wfv1Bx3PDZzFAgvtRrunYg2gefTBT9EUpYPIJSFiSvJtUPgtTDuW39ZTByzceqqVOobJJj6Gg%3d%3d; uidal=6182326063031944%e6%97%b6%e4%b8%8d%e6%88%91%e5%be%8513; sid=153447085; vtpst=|; em_hq_fls=js; st_si=45562855629372; st_asi=delete; waptgshowtime=20201210; HAList=a-sz-000001-%u5E73%u5B89%u94F6%u884C%2Ca-sz-300059-%u4E1C%u65B9%u8D22%u5BCC%2Ca-sh-600000-%u6D66%u53D1%u94F6%u884C; st_pvi=52532572402789; st_sp=2020-11-24%2013%3A10%3A23; st_inirUrl=https%3A%2F%2Fwww.baidu.com%2Fs; st_sn=18; st_psi=20201210210529282-113200301201-2186077488"
                request.headers['Cookie'] = cookies  # 手动设置cookies，不一定能用
                redis.set("stocksCookies", cookies.encode())  # 添加进Redis中
                
                
"""-----------------------------------------------------------------"""






"""---------------------------爬虫中间件-----------------------------"""

"""-----------------------------------------------------------------"""





























class StocksSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class StocksDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
