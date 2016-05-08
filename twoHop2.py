#-*- coding:utf-8 -*-
"""
The given pair of entity identifiers could be 
[Id, Id], [Id, AA.AuId], [AA.AuId, Id], [AA.AuId, AA.AuId]. 
Each node of a path should be one of the following identifiers: 
Id, F.Fid, J.JId, C.CId, AA.AuId, AA.AfId. 
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
	#print(list_sum)
        self.id_set = set(list_sum)    

    def query_as_AuId(self):
        try:
            expr = "expr=composite(AA.AuId=%s)&count=10000&attributes=Id,AA.AfId"%self.id1
            api_return = query_api(expr)
            res_json = json.loads(api_return)
	    if "Id" in res_json["entities"][0]:
                for i in res_json["entities"][0]["Id"]:
                    self.Id_list.append(i['Id'])
	    elif "AA" in res_json["entities"][0]:
                for i in res_json["entities"][0]["AA"]:
                    if "AfId" in i:
                        self.AfId_list.append(i["AfId"])
	    else:
	  	query_as_ID(self)           
	    return( 0,set(self.Id_list),set(self.AfId_list) )
        except Exception as e:
            return("Query auid" + str(e))
            
    def query_as_Id(self):
            expr = "expr=Id=%s&count=10000&attributes=Id,AA.AuId,AA.AfId,RId,C.CId,F.FId,J.JId"%self.id1
            api_return = query_api(expr)
            res_json = json.loads(api_return)
            #return api_return
            if "AA" in res_json["entities"][0]:
                for i in res_json["entities"][0]["AA"]:
                    self.AuId_list.append(i['AuId'])                  
            if "F" in res_json["entities"][0]:
                for i in res_json["entities"][0]["F"]:
                    self.FId_list.append(i["FId"])
            if "J" in res_json["entities"][0]:
                    self.JId_list.append(res_json["entities"][0]["J"]["JId"])
            if "C" in res_json["entities"][0]:        
                self.CId_list.append(res_json["entities"][0]["C"]["CId"])
            if "RId" in res_json["entities"][0]:
                self.RId_list.extend(res_json["entities"][0]["RId"])
            self.id_union()
            #return list(self.id_set)#AuId_list
            return( 1,self.id_set,set(self.RId_list) )


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
    IA = idAnalysor(id1,id2)
    (isId1,id_set_A1,id_set_A2) = IA.query_as_AuId()
    IB = idAnalysor(id2,id2)
    (isId2,id_set_B1,id_set_B2) = IB.query_as_AuId()
    if isId1==1 and isId2==1:
        intersection = id_set_A1 & id_set_B1
        two_hop_path_list = []
        for i in intersection:
	    two_hop_path_list.append([int(id1),i,int(id2)])
	#这里还应该有处理RId的语句
    elif isId1==1 and isId2==0:
	for i in IA.RId_list:
	    #查询对应的AuId
	    pass
    elif isId1==0 and isId2==1:
        for i in IB.RId_list:
	    #查询对应的AuId
	    pass
    else:
        intersection = id_set_A1 & id_set_B1#经Id的路径
        two_hop_path_list = []
        for i in intersection:
	    two_hop_path_list.append([int(id1),i,int(id2)])
	intersection = id_set_A2 & id_set_B2#经AfId的路径
	for i in intersection:
	    two_hop_path_list.append([int(id1),i,int(id2)])    
    return two_hop_path_list
    
if __name__ == "__main__":
    id1=2151561903
    id2=2015720094
    print("twoHop test")
    start_time = datetime.now()
    result = getPath(id1,id2)
    print(result)
    delta = datetime.now() - start_time
    print("\nCost time: %s ms"%(str(delta.microseconds/1000)))
    
