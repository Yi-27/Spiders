import scrapy
import time
import json
import pandas as pd

class DongfangcaifuranklistSpider(scrapy.Spider):
    name = 'DongfangcaifuRankList'
    allowed_domains = ['69.push2.eastmoney.com/api/qt/clist/get?']
    start_urls = ['http://69.push2.eastmoney.com/api/qt/clist/get?']

    headers = {
        "Cookie": "qgqp_b_id=498c8ab46440318862f8757ff37ca2aa; cowCookie=true; cowminicookie=true; intellpositionL=1522.39px; em_hq_fls=js; em-quote-version=topspeed; intellpositionT=736px; st_si=28370171622833; st_asi=delete; p_origin=https%3A%2F%2Fpassport2.eastmoney.com; ct=Ombkf0Kj9RGhrxqSG3K_tMfx6ogxzD16IwaftTT2T4M4B-9SZFM_Qw5IR8mpfffmcbgiN-yJmp2fFtPrWYq5OmuHGERNA5fuMfguiCCHUp1IMjn0WSQRPslxCpKOESc0XBBr3PjQsVUHxC04pzPEbaxGMXPFQXQk3vjOAHAZ_q0; ut=FobyicMgeV7bfas_M05TDBOeyCFFs48knKwC5VBjLh4OQceJBUzUsQihFbc8gUi_5OPQwgb3yLNkDoEO-0b-qSRrv6swX_WeiFe1bMQk9dFXwUVQLPPG3AI_grbg8Kj9CS-4nHIh0D7f4atKAtC1Kmm9UwSPBCwGsdrV2HUYNkfPjiQsNg0I4czRn1MDjrZ1gv79YMZPw0XXw9nQ827regRez-AZzdQWQSVJFrp53OtMdnk9uL0PBKqVm8rsBbPFChljf8TvHb3RGW9VkijNWYuiOffA7MRI; sid=153447085; uidal=6182326063031944%e6%97%b6%e4%b8%8d%e6%88%91%e5%be%8513; pi=6182326063031944%3bg6182326063031944%3b%e6%97%b6%e4%b8%8d%e6%88%91%e5%be%8513%3bhjhcVFCD3Qiif891DXIAWPWyLfnJ%2f1C6eyuk7yVTObnVCjEyAVQWwKXaIf%2bY5dBDJQarpaYlHrsbDl4DkXgJWNsjLJD9qZqJbN%2fos2EzJNZsJ%2fepKsjgV7BAUjsPsB8kvStm4nMNV2e2hEA%2biQvCTpMSUk%2b7W9%2fDuBXnTAH9NpKnpqRyX7WAkPZULDfBffn7RwESlVKu%3bN6G2daAElLngz%2bswB5Y9Ty1u7A2DSuIIG6ZAMQJtDd5Z7SwihNdXRu%2fw7dYO9ZOJ7djUD%2f50VcDN2T8umsox7k%2fG0e4REWOyQFnKBpe8VvBNt5jKqze3OAjL4uPv76z%2blzrrUp%2bBIRTA48dbsdAJM%2ff%2fuEovuQ%3d%3d; vtpst=|; waptgshowtime=20201126; HAList=a-sz-000003-PT%u91D1%u7530A%2Ca-sz-300059-%u4E1C%u65B9%u8D22%u5BCC%2Ca-sz-000001-%u5E73%u5B89%u94F6%u884C%2Cf-0-000001-%u4E0A%u8BC1%u6307%u6570%2Ca-sh-600000-%u6D66%u53D1%u94F6%u884C%2Ca-sh-688050-%u7231%u535A%u533B%u7597%2Ca-sz-000002-%u4E07%20%20%u79D1%uFF21%2Cf-0-399006-%u521B%u4E1A%u677F%u6307; st_pvi=52532572402789; st_sp=2020-11-24%2013%3A10%3A23; st_inirUrl=https%3A%2F%2Fwww.baidu.com%2Fs; st_sn=42; st_psi=20201126115446696-113200301201-4821065056",
        "Host": "push2.eastmoney.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36 Edg/87.0.664.41",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }
    with open("center.json", "r", encoding="utf-8") as f:
        params_list = json.load(f)  # 行情股票列表

    with open("filed_name.json", "r", encoding="utf-8") as f:
        filed_name = json.load(f)
    

    def start_requests(self):
        
        public_params = [
            "pn=1",  # 页数
            "po=0",  # 0 1 升序
            "np=1",  # 1 1 降序
            "ut=bd1d9ddb04089700cf9c27f6f7426281",
            "fltt=2",
            "invt=2",
            "fid=f12",  # 按代码排序
            "fields=f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f26",
        ]
        for p in self.params_list:
            cb = "cb=jQuery112404633069651159658_%s"%str(time.time()).replace(".", "")[:-4]
            timestamp = "_=%s" % str(time.time()).replace(".", "")[:-4]
            
            url = f"http://69.push2.eastmoney.com/api/qt/clist/get?{cb}&{'&'.join(public_params)}&{'&'.join(list(p.values())[0])}&{timestamp}"
            print(url)
            
            meta = {
                "_type": list(p.keys())[0]
            }
            
            yield scrapy.Request(url, headers=self.headers, callback=self.hs_parse,meta=meta, dont_filter=False) # 只爬一次

    def hs_parse(self, response, **kwargs):
        """用于处理沪深A股爬取到的数据"""
        res = response.text
        data_json = res[res.find("(") + 1:-2]  # 截取字符串，方便从json字符串转换成字典
        data_dict = json.loads(data_json)
        data = data_dict["data"]["diff"]  # 类型是[{},{},...]

        # 直接用pandas转成DataFrame
        data_pd = pd.DataFrame(data)
        data_pd.rename(columns=self.filed_name, inplace=True)
        data_pd.to_csv(f"./stocks/{response.meta['_type']}_{round(time.time())}.csv", encoding='GBK', index=False)


    def parse(self, response, **kwargs):
        pass
