import scrapy
import json
from lxml import html
from ..items import ProxyItem

class ZhimadailiSpider(scrapy.Spider):
    name = 'ZhimadailiSpider'
    allowed_domains = ['h.zhimaruanjian.com/']
    start_urls = ['http://h.zhimaruanjian.com/']
    
    
    headers = {
        "Cookie": "PHPSESSID=8u261blvva6cohgvr242j4g9u5;",
        "Host": "wapi.http.cnapi.cc",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Content-Length": "6",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
    }
    
    def start_requests(self):
        for i in range(1, 6):
            self.logger.info(f"返回第 {i} 个 URL")
            yield scrapy.Request("http://wapi.http.cnapi.cc/index/index/get_free_ip?page=%s"%i,
                                headers=self.headers,
                                callback=self.proxy__check_parse,
                                dont_filter=False)

    def proxy__check_parse(self, response):
        self.logger.info("开始处理 %s !", response.url)
        
        res_html = json.loads(response.text)["ret_data"]["html"]
        res_html = html.etree.HTML(res_html)
        ip_list = res_html.xpath("//tr[@class='tr']/td[1]/text()")
        port_list = res_html.xpath("//tr[@class='tr']/td[2]/text()")
        scheme_list = res_html.xpath("//tr[@class='tr']/td[4]/text()")

        print(ip_list)
        print(port_list)
        print(scheme_list)
        
        #
        for i in range(len(ip_list)):
            scheme = scheme_list[i]
            ip = ip_list[i]
            port = port_list[i]
            
            url = '%s://httpbin.org/ip' % scheme
            proxy = '%s://%s:%s' % (scheme, ip, port)
    
            # meta用于放请求的元数据和 向返回中传递数据
            meta = {
                "proxy": proxy,
                'dont_retry"': True,
                'download_timeout': 10,
                # 以下字段是用于存储的
                '_proxy_scheme': scheme,
                '_proxy_ip': ip,
                "_proxy_port": port,
            }
    
            yield scrapy.Request(url, callback=self.proxy_parse, meta=meta, dont_filter=True)

    def proxy_parse(self, response):
        """最终确定可要将IP存下来"""
        self.logger.info("准备存储 %s !" % response.url)
        # 提取存在meta中的数据
        proxy_ip = response.meta["_proxy_ip"]
        # 判断代理是否具有隐藏IP功能？？？
        if proxy_ip == json.loads(response.text)["origin"]:
            print(proxy_ip, " 可以用！")
        
            # 写进日志中，表明要生成实体对象了
            self.logger.info("代理实体对象 %s 将被创建!", proxy_ip)
        
            # 为这个数据项构建实体对象
            proxy = ProxyItem()
            proxy["ip"] = proxy_ip
            proxy["port"] = response.meta["_proxy_port"]
            proxy["scheme"] = response.meta["_proxy_scheme"]
            # proxy["time"] = time.time()  # 记录生成实体对象的时间
        
            yield proxy  # 将这个创建的proxy实体对象返回
        else:
            print(proxy_ip, " 不可以用啊！！")

    def parse(self, response, **kwargs):
        pass
