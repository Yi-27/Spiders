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
import time
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By


"""---------------------------下载中间件-----------------------------"""
# 随机代理中间件下载中间件
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


# 随机设置UA  下载中间件
class RandomUserAgentMiddleware(object):  # 下载中间件
    
    def __init__(self):
        self.ua = UserAgent()
    
    def process_request(self, request, spider):
        # 设置随机的UA
        request.headers["User-Agent"] = self.ua.random


# 设置行情中心爬虫的headers
# 需要注意该下载中间件的优先级要比随机设置UA的下载中间件要高一点
class HQZXHeadersMiddleware(object):
    
    def process_request(self, request, spider):
        if spider.name == "hangqingzhongxin":
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
            request.headers = {**request.headers, **headers} # 合并两个字典


# 模拟东方财富网站登录的中间件  下载中间件
class LoginDFCFMiddleware(object):  # 下载中间件
    """使用selenium模拟登录，并跳转到需要爬取的页面，并获取cookies，和要爬取的url"""
    
    def process_request(self, request, spider):
        """在正式发送请求前执行该方法"""
        if spider.name == "hangqingzhongxin":
            # 模拟登陆
            driver = spider.driver  # selenium的Driver放在Spider中
            driver.get("https://passport2.eastmoney.com/pub/login?backurl=")
            # z找到用户名和密码框
            username = driver.find_element_by_name('login_email')
            password = driver.find_element_by_name('login_password')
            loginbtn = driver.find_element_by_class_name('loginBtn')
    
            # 表单左右栏body > div > div.loginTabClass /html/body/div/div[1]/span[1]
            right_span = driver.find_element_by_css_selector("div.loginTabClass > :nth-child(2)")
            left_span = driver.find_element_by_css_selector("div.loginTabClass > :nth-child(1)")
    
            # 填写表单
            try:
                ActionChains(driver).move_to_element(username).perform()
                username.click()
                time.sleep(0.5)  # 睡0.5秒不至于执行那么快
                username.send_keys("763074310@qq.com")
                password.send_keys("123456")
            except Exception as e:
                print(e)
                # 出错就再试一次
                print("再试一次")
                try:
                    ActionChains(driver).move_to_element(username).perform()
                    username.click()
                    time.sleep(1)  # 睡0.5秒不至于执行那么快
                    username.send_keys("763074310@qq.com")
                    password.send_keys("jiyou0612")
                except Exception as e2:
                    print("还是失败了！")
            
            # 先悬浮在右标签上 account title 再浮会表单页即可显示验证按钮
            ActionChains(driver).move_to_element(right_span).move_to_element(left_span).perform()
            time.sleep(0.5)  # 睡0.5秒不至于执行那么快
            # 定位验证按钮
            verify_btn = driver.find_element_by_css_selector("#div_vcode")
            verify_btn.click()  # 点击验证按钮，验证成功即可进入页面
            
            try:
                logout = driver.find_element_by_css_selector("#headlogout")
                if(logout.is_enabled()):
                    print("登陆成功！")
                else:
                    print("出现错误")
            except Exception as e:
                print(e)
                print("登陆失败")
                
            # 登陆成功后就跳转到行情中心页面，获取cookies并存储到redis中
            driver.get("http://quote.eastmoney.com/center/gridlist.html#hs_a_board")
            cookies = driver.get_cookies()  # 是个列表[{},{},...]
            
            # 从Spider中获取redis，将Cookies存储到redis中
            redis = spider.redis
            redis.hmset("dfcfCookies", json.dumps(cookies))
        
        
# 设置cookies
class DFCFSetCookiesMiddleware(object):
    
    def process_request(self, request, spider):
        if spider.name == "hangqingzhongxin":
            redis = spider.redis
            if redis.exists("dfcfCookies"):
                request.cookies = json.loads(redis.get("dfcfCookies").decode())  # 设置cookies
            else:
                request.headers['Cookie'] = "qgqp_b_id=498c8ab46440318862f8757ff37ca2aa; p_origin=https%3A%2F%2Fpassport2.eastmoney.com; ct=w_B6TvJKJO7UPRJ6YKT2QUw8s2AyFzSa2XMmQaZcI8BekRAwdmJOIof9H9EAka_-MiwpNVRO-PYpnfc98NRAYBqiapknw8EQxMDXtaaFEsuOitvr3E-EHHXjQbAk3POnAge6GfwVpag8aiheONdGeiIn7g65U89CTfeMaIX3eFE; ut=FobyicMgeV7bfas_M05TDBOeyCFFs48knKwC5VBjLh4OQceJBUzUsQihFbc8gUi_5OPQwgb3yLNkDoEO-0b-qSRrv6swX_WeiFe1bMQk9dFXwUVQLPPG3AI_grbg8Kj9CS-4nHIh0D7f4atKAtC1Kmm9UwSPBCwGsdrV2HUYNkfPjiQsNg0I4czRn1MDjrZ1gv79YMZPw0XXw9nQ827repkX_joNWr0srtn_aZ2Ioo3ISdXfCAjd6JJEf35rsxI805TlXeq9EmUaL4ZFQG0d-DsNYpAaNmp8; pi=6182326063031944%3bg6182326063031944%3b%e6%97%b6%e4%b8%8d%e6%88%91%e5%be%8513%3byGhidakwmMWJe8NKgZzCwcSV%2bUie8tSW4OQ%2boskTA0fAE%2fLWthaNsq%2f9Vwka5Ypb27xTmZRMn9k83a1U8QK0CHZO6aTsi2BMxLFTi7Qt3a7k4DoC7aPRL3NOCG%2bY0oFE0ZhtqKmvbJt65gslq180jNqOugSedTxQrjeC%2f%2fNLANB3RxK2tVTQRfqM5zqHEjk%2bW76tG6k2%3bxnG03MNdfN6cj9SYk9JOElakwC8Hwm5zKsKG5Mh9xjVfIly7900UONCBn1bYa%2bAbLwc0fSety6ndiLqjhSkobik70ZPzmYOrN%2bLjWcdJCh4vhE84H4r92O79MZDN4reSrR%2fcZ2nMeXqo6Qsp9ofr88bFfULYdQ%3d%3d; uidal=6182326063031944%e6%97%b6%e4%b8%8d%e6%88%91%e5%be%8513; sid=153447085; vtpst=|; testtc=0.2904408531600091; st_si=81210525039055; st_asi=delete; st_pvi=18132808206149; st_sp=2020-12-06%2020%3A23%3A41; st_inirUrl=http%3A%2F%2Fquote.eastmoney.com%2Fcenter%2F; st_sn=3; st_psi=20201206204259824-113200301321-4620583248"  # 手动设置cookies，不一定能用
        

# 下载中间件模板流程
class MyDownloaderMiddleware(object):
    @classmethod
    def from_crawler(cls, crawler):
        # 调用此 类方法，根据crawler创建一个该middleware的实例对象，
        # 通过crawler可以获取settings和signals等。这是中间件访问它们并将其功能连接到Scrapy中的一种方式
        # 比如crawler.settings.get('HTTPPROXY_PROXY_LIST_FILE')
        # return cls() 返回时要实例化一个当前中间件对象
        pass
    def process_request(self, request, spider):
        # 每个request都会调用downloader中间件的此方法。
        # 注意！此时还没真正的向url发送请求

        # 为通过该中间件的每个请求调用，可以通过spider的名称来过滤
        # 中间件。
        # 必须：
        # -return None:继续处理此请求，不返回默认返回None
        # —或返回 响应对象
        # —或返回 请求对象
        # —或引发IgnoreRequest:的process_exception（）方法
        # 继续处理请求是会接着调用下面的中间件
        pass
    def process_response(self, request, response, spider):
        # 每个response都会调用downloader中间件的此方法。
        # 注意！此时是真正请求url后得到的响应
        
        # 必须：
        # -返回响应对象
        # -返回请求对象
        # -或提出IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # 当download handler或者 process_request()方法raise异常的话，Scrapy 会调用每一个downloader中间件的此方法。
        pass

"""-----------------------------------------------------------------"""




"""---------------------------爬虫中间件-----------------------------"""
class HQZXKafkaMiddleware(object):
    """行情中心的数据被爬取到返回后，先通过该方法，再返回给数据库"""
    
    def process_spider_input(self, response, spider):
        """
        这里将响应的数据中的data（每条股票的在行情中心中对应的数据）提取出来
        存放在Kafka中，对应的
        """
        if spider.name == "hangqingzhongxin":
            res = response.text
            data_json = res[res.find("(") + 1:-2]  # 截取字符串，方便从json字符串转换成字典
            data_dict = json.loads(data_json)
            data = data_dict["data"]["diff"]  # 类型是[{},{},...]
            
            type = response.meta['_type']  # 获取类型，用于指定
            # 获取到一个异步生产者，用于存爬取到的数据
            producer = spider.kafka.get_producer(type)
            
            # 往kafka中写数据
            for row in data:
                producer.produce(json.dumps(row).encode())


class HQZXMongoMiddleware(object):
    """行情中心的数据持久化存储到mongoDB中"""
    def process_spider_input(self, response, spider):
        if spider.name == "hangqingzhongxin":
            mongo = spider.mongo
            # 指定数据库
            db = mongo["hqzx"]
            # 获取指定集合
            collection = db[response.meta["_type"]]

            res = response.text
            data_json = res[res.find("(") + 1:-2]  # 截取字符串，方便从json字符串转换成字典
            data_dict = json.loads(data_json)
            data = data_dict["data"]["diff"]  # 类型是[{},{},...]

            collection.insert_many(data)  # 批量写入mongoDB中


class HQZXRedisMiddleware(object):
    """将从行情中心爬到的所有股票放进Linux中的Redis数据库中，方便之后的爬虫股票的时间信息"""
    
    def process_spider_input(self, response, spider):
        if spider.name == "hangqingzhongxin":
            redis = spider.linux_redis

            res = response.text
            data_json = res[res.find("(") + 1:-2]  # 截取字符串，方便从json字符串转换成字典
            data_dict = json.loads(data_json)
            data = data_dict["data"]["diff"]  # 类型是[{},{},...]

            for d in data:
                redis.sadd("stockList", {"name": d["f14"], "code": d["f12"]})  # 写入redis中
    
    
class HQZXStorageMiddleware(object):
    """将数据存储到Redis、MongoDB、Kafka中"""
    def process_spider_input(self, response, spider):
        if spider.name == "hangqingzhongxin":
            redis = spider.linux_redis

            res = response.text
            data_json = res[res.find("(") + 1:-2]  # 截取字符串，方便从json字符串转换成字典
            data_dict = json.loads(data_json)
            data = data_dict["data"]["diff"]  # 类型是[{},{},...]

            type = response.meta['_type']  # 获取类型，用于指定

            self.redis_save(data, redis)
            self.mongo_save(data, spider.mongo, type)
            self.kafka_save(data, spider.kafka, type)

    def redis_save(self, data, redis):
        """将股票存储到Redis队列中"""
        for d in data:
            redis.sadd("stockList", {"name": d["f14"], "code": d["f12"]})  # 写入redis中
        
    def mongo_save(self, data, mongo, type):
        # 指定数据库
        db = mongo["hqzx"]
        # 获取指定集合
        collection = db[type]
        collection.insert_many(data)  # 批量写入mongoDB中
        
    def kafka_save(self, data, kafka, type):
        # 获取到一个异步生产者，用于存爬取到的数据
        producer = kafka.get_producer(type)
    
        # 往kafka中写数据
        for row in data:
            producer.produce(json.dumps(row).encode())

# 爬虫中间件模板流程
class MySpiderMiddleware(object):
    @classmethod
    def from_crawler(cls, crawler):
        # 调用此方法创建一个中间件的实例。此方法必须返回一个中间的的实例对象。
        # 同下载中间件这里差不多
        return cls()
    
    def spider_opened(self, spider):  # 爬虫开始
        spider.logger.info('Spider opened: %s' % spider.name)
        
    def process_spider_input(self, response, spider):
        # response返回给spider前，会通过该中间件，调用该方法
        # 应返回None或引发异常。
        pass
    def process_spider_output(self, response, result, spider):
        # spider处理完response之后，从spider返回result后，就该调用中间件的此方法。
        # 即在Spider中调用完响应的parse后，就接着调用该方法
        # 应返回可迭代的请求，item对象
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # 当Spider或process_spider_output（）方法（来自先前的Spider中间件）引发异常时，将调用此方法。
        pass

    def process_start_request(self, start_requests, spider):
        # 以spider的start repsponse为参数调用此方法，工作原理与process_spider_output()相似。
        # 不同之处在于，它没有关联的response，必须返回requests。
        for i in start_requests:
            yield i

"""-----------------------------------------------------------------"""



















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