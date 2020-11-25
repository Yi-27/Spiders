str = "HTTP代理"
str = str[:-2]
print(str)
h = str.split(",")
print(h)

import datetime

print(datetime.datetime.now())
import time
print(time.time())
print(round(time.time()))
import requests
import json, re
from lxml.html import etree


headers = {
    #                                                                                                                                                                                     1606283621
    # csrftoken=hRFTMYZnea1k5wDjTvF550le8EBv7Js1IvZEaYJT3ZjvjcxEZU5evbaGHdicNy7j; Hm_lvt_9bfa8deaeafc6083c5e4683d7892f23d=1606218274,1606281092; Hm_lpvt_9bfa8deaeafc6083c5e4683d7892f23d=1606283030
    # "Cookie":                                                                  "Hm_lvt_9bfa8deaeafc6083c5e4683d7892f23d=1606230219;            Hm_lpvt_9bfa8deaeafc6083c5e4683d7892f23d=1606232784",
    # "Cookie": "csrftoken=hRFTMYZnea1k5wDjTvF550le8EBv7Js1IvZEaYJT3ZjvjcxEZU5evbaGHdicNy7j; Hm_lvt_9bfa8deaeafc6083c5e4683d7892f23d=%s; Hm_lpvt_9bfa8deaeafc6083c5e4683d7892f23d=%s"%(round(time.time()), round(time.time())),
    # "Cookie": "_uab_collina=160621801601536460112883; __root_domain_v=.zhimaruanjian.com; _qddaz=QD.ly03fe.tczh80.khvwqhrj; UM_distinctid=175fa0de884c04-07f915a9c4aba6-930346c-1fa400-175fa0de885ca1; Hm_lvt_53b4ff1c2dbe5fda8716f55c5e85716b=1606219090,1606281121; Hm_lpvt_53b4ff1c2dbe5fda8716f55c5e85716b=1606281121; Hm_lvt_3c109d429e947ddb881d462fbeaacfbf=1606219090,1606281121; Hm_lpvt_3c109d429e947ddb881d462fbeaacfbf=1606281121; CNZZDATA1264405237=2069383313-1606213090-https%253A%252F%252Fwww.baidu.com%252F%7C1606279510; Hm_lvt_a1f04b432daf9b449b5cef46eb11a97b=1606218017,1606281938,1606281992; _qdda=3-1.2x78u4; _qddab=3-4b0of7.khx0da3j; Hm_lpvt_a1f04b432daf9b449b5cef46eb11a97b=1606284727; CNZZDATA1262305770=449048171-1606215773-https%253A%252F%252Fwww.baidu.com%252F%7C1606283615; CNZZDATA1272886568=1470220811-1606215857-https%253A%252F%252Fwww.baidu.com%252F%7C1606283615; CNZZDATA1264405238=113820174-1606215773-https%253A%252F%252Fwww.baidu.com%252F%7C1606283615",
    "Host": "wapi.http.cnapi.cc",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
}

res = requests.post("http://wapi.http.cnapi.cc/index/index/get_free_ip", headers=headers, data={"page": "1"})
print(res.text)
print(res.status_code)
print(res.cookies)
cookies = requests.utils.dict_from_cookiejar(res.cookies)
print(cookies)

res_html = json.loads(res.text)["ret_data"]["html"]
print(res_html)
pattern = "<td><span class=\"slogan\">FREE<\/span>(.*?)<\/td>.*<td>(.*?)<\/td>.*<td>(.*?)<\/td>.*?<td>(.*?)<\/td>"
print(re.findall(pattern, res_html))

html = etree.HTML(res_html)
ip_list = html.xpath("//tr[@class='tr']/td[1]/text()")
port_list = html.xpath("//tr[@class='tr']/td[2]/text()")
scheme_list = html.xpath("//tr[@class='tr']/td[4]/text()")

print(ip_list)
print(port_list)
print(scheme_list)