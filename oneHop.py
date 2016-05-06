#-*- coding:utf-8 -*-
"""
The given pair of entity identifiers could be 
[Id, Id], [Id, AA.AuId], [AA.AuId, Id], [AA.AuId, AA.AuId]. 
Each node of a path should be one of the following identifiers: 
Id, F.Fid, J.JId, C.CId, AA.AuId, AA.AfId. 

一跳的没写完，参考两跳，用到了python的字典set数据结构
你们多加油，不要被我写的东西束缚了思想,
代码水平有限，可读性可能不太好，有问题QQ留言，请多指教见谅~~
"""
from datetime import datetime
import urllib
import json
import oneHop

url_head = "https://oxfordhk.azure-api.net/academic/v1.0/evaluate?"
key_info = "&subscription-key=f7cc29509a8443c5b3a5e56b0e38b5a6"

class idAnalysor:
    def __init__(self,id1,id2):
        self.id1 = id1
        self.id2 = id2
        self.id_set = set()
        self.AuId_list = []
        self.RId_list = []
        self.AfId_list = []
        self.CId_list = []
        self.JId_list = []
        self.FId_list = []
        
    def id_union(self):
        list_sum = self.AuId_list + self.RId_list +self.CId_list +self.JId_list +self.AfId_list +self.FId_list
        self.id_set = set(list_sum)    
        
#不完整
    def query_as_auid(self):
        try:
            expr = "expr=composite(AA.AuId=%s)&count=10000&attributes=Id,AA.AfId, C.CId, AA.AuId, AA.AfId"%self.id1
            api_return = query_api(expr)
            res_json = json.loads(api_return)
            return api_return
        except Exception as e:
            return("Query auid" + str(e))
            
    def query_as_ID(self):
            test_expr = "expr=Id=%s&count=10000&attributes=Id,AA.AuId,AA.AfId,RId,C.CId,F.FId,J.JId"%self.id1 #for test
            expr = test_expr
            api_return = query_api(expr)
            res_json = json.loads(api_return)
            #return api_return
            if "AA" in res_json["entities"][0]:
                for i in res_json["entities"][0]["AA"]:
                    self.AuId_list.append(i['AuId'])
                    if "AfId" in i:
                        self.AfId_list.append(i["AfId"])
            if "F" in res_json["entities"][0]:
                for i in res_json["entities"][0]["F"]:
                    self.FId_list.append(i["FId"])
            if "J" in res_json["entities"][0]:
                    self.JId_list.append(res_json["entities"][0]["J"]["JId"])
            if "C" in res_json["entities"][0]:        
                self.CId_list.append(res_json["entities"][0]["C"])
            if "RId" in res_json["entities"][0]:
                self.RId_list.extend(res_json["entities"][0]["RId"])
            self.id_union()
            #return list(self.id_set)#AuId_list
            return self.id_set


#输入查询语句访问api，返回文本
def  query_api(expr):
        try:
            obj_url = url_head + expr + key_info
            req = urllib.urlopen(obj_url)
            result = req.read()
            #res_json = json.loads(html_result)
            return result
        except Exception as e:
            return("Query exception" + str(e))
            
def getPath(id1,id2):
    pass
    
if __name__ == "__main__":
#单元测试，不过可能不需要
    id1=2147152072
    id2=189831743
    print("oneHop test")
    start_time = datetime.now()
    result = getPath(id1,id2)
    print(result)
    delta = datetime.now() - start_time
    print("\nCost time: %s ms"%(str(delta.microseconds/1000)))
    