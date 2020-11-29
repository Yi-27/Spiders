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
from fake_useragent import UserAgent
import redis
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time



# 随机代理中间件
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


# 随机设置UA
class RandomUserAgentMiddleware(object):
    
    def __init__(self):
        self.ua = UserAgent()
    
    def process_request(self, request, spider):
        # 设置随机的UA
        request.headers["User-Agent"] = self.ua.random


# 模拟东方财富网站登录的中间件
class LoginDFCFMiddleware(object):
    """使用selenium模拟登录，并跳转到需要爬取的页面，并获取cookies，和要爬取的url"""
    
    def __init__(self):
        self.client = redis.StrictRedis()  # 连接Redis
        
        options = webdriver.ChromeOptions()
        options.add_argument("headless")  # 无窗口
        self.driver = webdriver.Chrome(executable_path="./chromedriver.exe", options=options)
    
    def process_request(self, request, spider):
        """在正式发送请求前执行该方法"""
        # 模拟登陆
        self.driver.get("https://passport2.eastmoney.com/pub/login?backurl=")
        # z找到用户名和密码框
        username = self.driver.find_element_by_name('login_email')
        password = self.driver.find_element_by_name('login_password')
        loginbtn = self.driver.find_element_by_class_name('loginBtn')

        # 表单左右栏body > div > div.loginTabClass /html/body/div/div[1]/span[1]
        right_span = self.driver.find_element_by_css_selector("div.loginTabClass > :nth-child(2)")
        left_span = self.driver.find_element_by_css_selector("div.loginTabClass > :nth-child(1)")

        # 填写表单
        try:
            ActionChains(self.driver).move_to_element(username).perform()
            username.click()
            time.sleep(0.5)  # 睡0.5秒不至于执行那么快
            username.send_keys("763074310@qq.com")
            password.send_keys("jiyou0612")
        except Exception as e:
            print(e)
            # 出错就再试一次
            print("再试一次")
            try:
                ActionChains(self.driver).move_to_element(username).perform()
                username.click()
                time.sleep(1)  # 睡0.5秒不至于执行那么快
                username.send_keys("763074310@qq.com")
                password.send_keys("jiyou0612")
            except Exception as e2:
                print("还是失败了！")
        
        # 先悬浮在右标签上 account title 再浮会表单页即可显示验证按钮
        ActionChains(self.driver).move_to_element(right_span).move_to_element(left_span).perform()
        time.sleep(0.5)  # 睡0.5秒不至于执行那么快
        # 定位验证按钮
        verify_btn = self.driver.find_element_by_css_selector("#div_vcode")
        verify_btn.click()  # 点击验证按钮，验证成功即可进入页面
        
        try:
            logout = self.driver.find_element_by_css_selector("#headlogout")
            if(logout.is_enabled()):
                print("登陆成功！")
            else:
                print("出现错误")
        except Exception as e:
            print(e)
            print("登陆失败")
            
        # 登陆成功后就跳转到行情中心页面，获取cookies并存储到redis中
        self.driver.get("http://quote.eastmoney.com/center/gridlist.html#hs_a_board")
        cookies = self.driver.get_cookies()
        



# 对于东方财富上的其他URL的爬取，用该cookies中间件给每个请求加上Cookies
class DFCFRequestsCookiesMiddleware(object):
    """需要用到的cookies存储在Redis中，这里就是动态从中取出来"""
    
    def __init__(self):
        self.client = redis.StrictRedis()  # 连接Redis
        
    def process_request(self, request, spider):
        cookies = json.loads(self.client.lpop("dfcf_cookies").decode())
        request.cookies = cookies



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


# 随机选取代理的下载中间件  该方法过时了！！！
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