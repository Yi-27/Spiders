# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter

from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware
from collections import defaultdict
import json
import random


# 随机选取代理的下载中间件
class RandomHttpProxyMiddleware(HttpProxyMiddleware):

    def __init__(self,auth_encoding='latin-1',proxy_list_file=None):
        if not proxy_list_file:
            # raise NotConfigured
            pass

        self.auth_encoding = auth_encoding  # 编码，默认时latin-1 ISO-8859-1
        # 分别用两个列表维护HTTP和HTTPS的代理，{'http':[...],'https':[...]}
        self.proxies = defaultdict(list)  # 初始化dict_list


        # 从json文件中读取代理服务器信息，填入self.proxies
        with open(proxy_list_file) as f:
            proxy_list = json.load(f)
            for proxy in proxy_list:
                scheme = proxy['scheme']  # http 或 https
                url = '%s://%s:%s' % (scheme, proxy["ip"], proxy["port"])  # "http://110.52.235.158:9999"
                self.proxies[scheme].append(self._get_proxy(url,scheme))  # 按种类添加


    @classmethod
    def from_crawler(cls,crawler):  # 开始爬虫时
        # 从配置文件中读取用户验证信息的编码
        auth_encoding = crawler.settings.get('HTTPPROXY_AUTH_ENCODING','latin-1')

        # 从配置文件中读取代理服务器列表文件(json)的路径
        proxy_list_file = crawler.settings.get('HTTPPROXY_PROXY_LIST_FILE')

        return cls(auth_encoding,proxy_list_file)


    def _set_proxy(self,request,scheme):
        # 随机选择一个代理
        creds,proxy = random.choice(self.proxies[scheme])
        request.meta['proxy'] = proxy  # 设置代理  爬虫时回自动使用这个中间件
        if creds:
            request.headers['Proxy-Authorization'] = b'Basic' + creds



# 随机代理
class ProxyMiddleware(object):
    # 设置Proxy
    def __init__(self, proxy_list_file=None):
        self.ip = []  # 初始化dict_list

        # 从json文件中读取代理服务器信息，填入self.proxies
        with open(proxy_list_file) as f:
            proxy_list = json.load(f)
            for proxy in proxy_list:
                scheme = proxy['scheme']  # http 或 https
                url = '%s://%s:%s' % (scheme, proxy["ip"], proxy["port"])  # "http://110.52.235.158:9999"
                self.ip.append(url)  # 按种类添加
        print(self.ip)
        
    @classmethod
    def from_crawler(cls, crawler):
        # 从配置文件中读取代理服务器列表文件(json)的路径
        proxy_list_file = crawler.settings.get('HTTPPROXY_PROXY_LIST_FILE')
        
        return cls(proxy_list_file)
    
    def process_request(self, request, spider):
        """在爬虫执行前会调用该方法"""
        ip = random.choice(self.ip)
        request.meta['proxy'] = ip


class RotateUserAgentMiddleware(object):
    
    def __init__(self):
        self._ua = [
        
        ]
    
    def process_request(self, request, spider):
        # 设置随机的UA
        request.headers["User-Agent"] = random.choice(self._ua)






class TutorialSpiderMiddleware:
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


class TutorialDownloaderMiddleware:
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
