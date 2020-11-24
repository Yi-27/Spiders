import logging

import scrapy
from scrapy import Request
from ..items import ProxyItem
import time, json

class ProxySpider(scrapy.Spider):
    
    name = "ProxySpider"
    allowed_domains = ["xiladaili.com"]  # 只允许爬该域内的URL
    start_urls = [  # 没有指定要爬取的URL时，爬虫从这里开始依次爬取
        "http://www.xiladaili.com/gaoni/",  # 爬虫的起始URL就是这个
    ]
    
    headers = {
        "Cookie": "Hm_lvt_9bfa8deaeafc6083c5e4683d7892f23d=1606218274; csrftoken=hRFTMYZnea1k5wDjTvF550le8EBv7Js1IvZEaYJT3ZjvjcxEZU5evbaGHdicNy7j; Hm_lpvt_9bfa8deaeafc6083c5e4683d7892f23d=1606225263",
        "Host": "www.xiladaili.com",
    }
    
    def start_requests(self):
        """该方法必须返回一个iterable，其中包含对第一个URL的爬取请求"""
        # 爬取前五页的高匿IP
        for i in range(1, 6):
            print(f"返回第 {i} 个 URL")
            # 每次返回出去一个Request，当再调用start_requests时才会将下一个Request返回出去
            
            # callback指明请求返回的响应处理函数
            yield Request("http://www.xiladaili.com/gaoni/%s"%i, callback=self.proxy_check_parse,  dont_filter=True)
        
        
    def proxy_check_parse(self, response):
        """自定义处理函数"""
        
        # 写日志
        self.logger.info("A response from %s just arrived!", response.url)
        
        # 提取每条数据
        for td in response.xpath("table[@class='fl-table']//tr[position()>1]"):
            ip_port = td.css("td:nth-child(1)::text").get()  # 相对于有getall()
            ip, port = ip_port.split(":")
            
            # 代理协议，HTTP或HTTPS
            schemes = td.css("td:nth-child(2)::text").get()  # 替换了原来的extract_first() 其实就是引用了get
            # 示例：HTTP,HTTPS代理，去掉最后的代理两字，然后以 , 分隔字符串即可
            scheme_list = schemes[:-2].split(",")
            
            
            # 检查该IP是否可用,发送请求到http(s)://httpbin.org/ip
            for scheme in scheme_list:
                url = '%s://httpbin.org/ip' % scheme
                proxy = '%s://%s:%s' % (scheme, ip, port)
            
                # meta用于请求之间传递数据
                meta = {
                    "proxy": proxy,
                    'dont_retry"': True,
                    'download_timeout': 10,
                    # 以下两个字段是传递给check_available方法的信息，方便检测
                    '_proxy_scheme': scheme,
                    '_proxy_ip': ip,
                    "_proxy_port": port,
                    # "_proxy_check_time": time.time(),  # 代理最后检验时间戳
                }
            
                yield Request(url, callback=self.proxy_parse, meta=meta, dont_filter=True)
            
    def proxy_parse(self, response):
        """最终确定可要将IP存下来"""
        # 提取存在meta中的数据
        proxy_ip = response.meta("_proxy_ip")
        # 判断代理是否具有隐藏IP功能？？？
        if proxy_ip == json.loads(response.text)["origin"]:
            print(proxy_ip, " 可以用！")
            
            # 写进日志中，表明要生成实体对象了
            self.logger.info("Proxy %s will be created!", proxy_ip)

            # 为这个数据项构建实体对象
            proxy = ProxyItem()
            proxy["ip"] = proxy_ip
            proxy["port"] = response.meta("_proxy_ip")
            proxy["time"] = time.time()  # 记录生成实体对象的时间
            
            yield proxy  # 将这个创建的proxy实体对象返回
        
    def parse(self, response, **kwargs):
        """这是响应的默认处理方法
        可以返回爬取的数据或者其他URL
        该方法和其他响应处理方法（请求回调）都必须返回Request或者Item Object
        """
        # 先写日志
        self.logger.info("A response from %s just arrived!", response.url)
        yield response.text
        
    def log(self, message, level=logging.DEBUG, **kw):
        pass