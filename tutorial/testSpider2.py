# -*- coding: utf-8 -*-

import requests
import time
import json
import pandas


headers = {
    "Cookie": "qgqp_b_id=498c8ab46440318862f8757ff37ca2aa; st_si=05487577764736; p_origin=https%3A%2F%2Fpassport2.eastmoney.com; uidal=6182326063031944%e8%82%a1%e5%8f%8b62LJ618966; sid=153447085; vtpst=|; EmPaVCodeCo=8ef6419f090748f380bd1c8407d4cfba; ct=su3gOaa-js9ywHmJrR2Lw8CFVcbtirVZVt5lhPY-6r2wK62I9VuT0vjFJGKsI2F0sbh73QTbNvIpd1v2KTZJy16V_pCaZr3d3BIEA-M7kBquDJyOg5yLCZRaz5BRg8VznquSR9yI9lIfuAW3O0kon1r3HqMGXrKamm83x8T88hY; ut=FobyicMgeV7bfas_M05TDBOeyCFFs48knKwC5VBjLh4OQceJBUzUsQihFbc8gUi_5OPQwgb3yLNkDoEO-0b-qSRrv6swX_WeiFe1bMQk9dFXwUVQLPPG3AI_grbg8Kj9CS-4nHIh0D7f4atKAtC1Kmm9UwSPBCwGsdrV2HUYNkfPjiQsNg0I4czRn1MDjrZ1gv79YMZPw0XXw9nQ827reglStd2UvNdO8PyOMcrp3fX1bzeve6qV84BM6UMG12_ep1i-Ns6fldQXA6EHrVEQnEE6LOt6Tm2n; pi=6182326063031944%3bg6182326063031944%3b%e8%82%a1%e5%8f%8b62LJ618966%3bGNmAMoT%2bwI0hfSJlvoKDa%2bh6TB2iqDLrW271sjorpl7Rv3y6w%2bwb4wT%2bFgP8YBtyy5HwW9zPgWmWcmeiCUC1tfGrJhn3UeOQTcr%2bLwyAkAkwdVNqLmtwIltDlc8QvSJ5k2eOK3CGocv3hfPd%2fL7PX1S78juMd10oKlD%2ftFwJS3neDFGS86VmuUYs3mZ9glV%2fD3gcQPdB%3bKVtM2ccQlXywQsqg0skMBa87Of%2b0SrM5pqhvCpIfRvlrQdz5N7Iq2DxvPqVFT3HVHemaqPIv%2fUVia3XW5z0L1Mi5Uod1vP83LTndvyrwRnJFFDJ5WEDIXuxxqyJY6gg3hPVpyiffkmnipZqa%2bHmkBP4Q%2bsdQXw%3d%3d; testtc=0.5168114660406042; cowCookie=true; cowminicookie=true; intellpositionL=1522.39px; em_hq_fls=js; em-quote-version=topspeed; intellpositionT=455px; st_asi=delete; HAList=a-sz-000001-%u5E73%u5B89%u94F6%u884C%2Ca-sz-300059-%u4E1C%u65B9%u8D22%u5BCC%2Ca-sh-688050-%u7231%u535A%u533B%u7597%2Ca-sz-000002-%u4E07%20%20%u79D1%uFF21%2Cf-0-399006-%u521B%u4E1A%u677F%u6307%2Cf-0-000001-%u4E0A%u8BC1%u6307%u6570; st_pvi=52532572402789; st_sp=2020-11-24%2013%3A10%3A23; st_inirUrl=https%3A%2F%2Fwww.baidu.com%2Fs; st_sn=78; st_psi=20201125200841231-113200301202-3191168001",
    "Host": "push2.eastmoney.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36 Edg/87.0.664.41",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}

params = [
    "cb=jQuery112405158909820893314_%s"%round(time.time()),
    "fields1=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13",
    "fields2=f51,f52,f53,f54,f55,f56,f57,f58",
    "ut=fa5fd1943c7b386f172d6893dbfba10b",
    "ndays=1",
    "iscr=0",
    "iscca=0",
    "secid=0.000001", # 股票
    "_=%s"%str(round(time.time())),
]
url = "http://push2.eastmoney.com/api/qt/stock/trends2/get?" + "&".join(params)
print(url)

html = requests.get(url, headers=headers)

res = html.text
print(res)
print(type(res))

data_jsonStr = res[res.find("(")+1:-2] # 截取字符串
print(data_jsonStr)
data = json.loads(data_jsonStr)
print(data)
print(data["data"]["trends"])
print(type(data["data"]["trends"]))
print(len(data["data"]["trends"]))
for t in data["data"]["trends"]:
    print(t)
