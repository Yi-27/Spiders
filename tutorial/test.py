# -*- coding: utf-8 -*-

import json
import time


with open("center.json", "r", encoding="utf-8") as f:
    params_list = json.load(f)  # 行情股票列表

with open("filed_name.json", "r", encoding="utf-8") as f:
    filed_name = json.load(f)
    
public_params = [
            "pn=1",  # 页数
            "pz=4237",  # 一页的数量
            "po=0",
            "np=1",
            "ut=bd1d9ddb04089700cf9c27f6f7426281",
            "fltt=2",
            "invt=2",
            "fid=f12",
            "fs=m:0+t:6,m:0+t:13,m:0+t:80,m:1+t:2,m:1+t:23",
            "fields=f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f26",
        ]

for p in params_list:
    cb = "cb=jQuery112404633069651159658_%s" % str(time.time()).replace(".", "")[:-4]
    timestamp = "_=%s" % str(time.time()).replace(".", "")[:-4]
    
    url = f"http://69.push2.eastmoney.com/api/qt/clist/get?{cb}&{'&'.join(public_params)}&{'&'.join(list(p.values())[0])}&{timestamp}"
    print(url)
    
    meta = {
        "_type": p
    }
    