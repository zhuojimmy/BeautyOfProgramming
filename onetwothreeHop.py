#-*- coding:utf-8 -*-
"""
The given pair of entity identifiers could be 
[Id, Id], [Id, AA.AuId], [AA.AuId, Id], [AA.AuId, AA.AuId]. 
Each node of a path should be one of the following identifiers: 
Id, F.Fid, J.JId, C.CId, AA.AuId, AA.AfId. 

//刘坤  0509
对象添加了 is_id1_ID()，如果当前id1是ID类型则为True，否则为False
请求分析案例：
同样Id在不同情况（作为auid和id）下访问的结果
https://oxfordhk.azure-api.net/academic/v1.0/evaluate?expr=Id=621499171&count=10000&attributes=Id,AA.AuId,AA.AfId,C.CId&subscription-key=f7cc29509a8443c5b3a5e56b0e38b5a6
https://oxfordhk.azure-api.net/academic/v1.0/evaluate?expr=composite(AA.AuId=2140251882)&count=10000&attributes=Id,AA.AuId,AA.AfId,C.CId&subscription-key=f7cc29509a8443c5b3a5e56b0e38b5a6
https://oxfordhk.azure-api.net/academic/v1.0/evaluate?expr=Id=621499171&count=10000&attributes=Id,AA.AuId,AA.AfId,C.CId&subscription-key=f7cc29509a8443c5b3a5e56b0e38b5a6
https://oxfordhk.azure-api.net/academic/v1.0/evaluate?expr=composite(AA.AuId=2140251882)&count=10000&attributes=Id,AA.AuId,AA.AfId,C.CId&subscription-key=f7cc29509a8443c5b3a5e56b0e38b5a6
刘坤 0512
这个缓存只在当前进程有效
缓存中存储的是idAnalysor对象的一个集合，查询添加到query_as_auid中了，
你们在用的时候应该不用改代码
效果是:从 180s 到 150s 不知道是不是因为其他因素
感觉多线程才是王道    
ksl 0513
mend Id->AuId road
mend AfId_list bug

*//


"""
from datetime import datetime
import urllib
import json
from pathCache import pathCache

url_head = "https://oxfordhk.azure-api.net/academic/v1.0/evaluate?"
key_info = "&subscription-key=f7cc29509a8443c5b3a5e56b0e38b5a6"
cache = pathCache()

class idAnalysor:
    def __init__(self,id1,id2):
        self.id_or_AuId = 0  # 0 as id         1 as AuId 
        self.id1 = id1
        self.id2 = id2
        self.id_set = set()
        self.AuId_list = []
        self.RId_list = []
        self.AfId_list = []
        self.CId_list = []
        self.JId_list = []
        self.FId_list = []
        self.Id_list = []
#将从这个点查询到的所有ID汇总为一个集合  id_set,即所有相邻节点id集合，作为本次查询最终处理的步骤        
    def id_union(self):
        list_sum =self.Id_list + self.AuId_list + self.AfId_list+self.CId_list +self.JId_list +self.FId_list#delete the RId list, it is not a node
	#print(list_sum)
        self.id_set = set(list_sum)    

    def query_as_Id(self):              
            global COUNT            
            expr = "expr=Id=%s&count=%d&attributes=Id,AA.AuId,AA.AfId,RId,C.CId,F.FId,J.JId"%(self.id1,COUNT)
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
            
                   
    # url eg:https://oxfordhk.azure-api.net/academic/v1.0/evaluate?expr=composite(AA.AuId=1982462162)&count=10000&attributes=Id,AA.AuId,AA.AfId,C.CId&subscription-key=f7cc29509a8443c5b3a5e56b0e38b5a6
    def query_as_AuId(self):
        query_cache = cache.query_by_id(self.id1)#查询返回了一个IDanalysor对象
        if query_cache != -1:#命中
            self.id_set = query_cache.id_set
            self.AuId_list = query_cache.AuId_list
            self.RId_list = query_cache.RId_list
            self.AfId_list = query_cache.AfId_list
            self.CId_list = query_cache.CId_list
            self.JId_list = query_cache.JId_list
            self.FId_list = query_cache.FId_list
            self.Id_list = query_cache.Id_list
            return 
        global COUNT 
        expr = "expr=composite(AA.AuId=%s)&count=%d&attributes=Id,AA.AfId"%(self.id1,COUNT)
        api_return = query_api(expr)
        res_json = json.loads(api_return)
        #id1是AuId
        if len(res_json["entities"])>0:
            self.id_or_AuId = 1
            for i in res_json["entities"]:
                self.Id_list.append(i['Id'])               
                if "AA" in i:
                    for j in i["AA"]:
                        if("AuId" in j):
                            if(self.id1==j["AuId"] and "AfId" in j):
                                self.AfId_list.append(j["AfId"])
                       # if "AuId" in author:
                         #   self.AuId_list.append(author["AuId"]) 
            self.id_union()
            cache.add_node(self)
            #show cache>>>>>>>
            #for i in cache.node_set:  
            #    print (str(i.id_set))
            #<<<<<<<<<
        #id1不是AuId   
        else:
                self.id_or_AuId = 0
                self.query_as_Id()
                cache.add_node(self)


    def is_id1_ID(self):
        if self.id_or_AuId == 0:
            return True
        else:
            return False

    def query_as_RId(self): 
        expr = "expr=RId=%s&count=%d&attributes=Id"%(self.id1,COUNT)
        api_return = query_api(expr)
        res_json = json.loads(api_return)
        if len(res_json["entities"])>0:
            for i in res_json["entities"]:
                self.Id_list.append(i['Id'])
            """
      def query_as_FId(self):
        expr = "expr=composite(F.FId=%s)&count=COUNT&attributes=Id" %(self.id1,COUNT)
        api_return = query_api(expr)
        res_json = json.loads(api_return)      
        if len(res_json["entities"])>0:
            for i in res_json["entities"]:
                self.Id_list.append(i['Id'])
            cache.add_node(self)
    def query_as_CId(self):
        expr = "expr=composite(C.CId=%s)&count=COUNT&attributes=Id"%(self.id1,COUNT)
        api_return = query_api(expr)
        res_json = json.loads(api_return)
        Id_list = []
        if "entities" in res_json:
            for i in res_json["entities"]:
                self.Id_list.append(i['Id'])
            cache.add_node(self)   
           
    def query_as_JId(self):
        expr = "expr=composite(J.JId=%s)&count=COUNT&attributes=Id"%(self.id1,COUNT)
        api_return = query_api(expr)
        res_json = json.loads(api_return)
        Id_list = []
        if "entities" in res_json:
            for i in res_json["entities"]:
                self.Id_list.append(i['Id'])       
        cache.add_node(self)        
         """
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
    global COUNT 
    COUNT = 10000
    IA = idAnalysor(id1,id2)
    IA.query_as_AuId()
    IB = idAnalysor(id2,id1)
    IB.query_as_AuId()
    #单跳
    one_hop_path = []
    if id2 in IA.RId_list:
        one_hop_path = [[id1,id2]]
    elif id2 in IA.Id_list or id1 in IB.Id_list:
        one_hop_path = [[id1,id2]]
    #两跳
    two_hop_path_list = []
    intersection = IA.id_set & IB.id_set
    for i in intersection:
        two_hop_path_list.append([int(id1),i,int(id2)])

    #1+1 or 1+2  or 1+1+1
    COUNT= 100
    three_hop_path_list = []

   #if next=Id,AuId
    if IA.is_id1_ID():#is Id
        next_set = set(IA.RId_list+IA.AuId_list)
    else:
        next_set = set(IA.Id_list)      
    for i in next_set:
        IA_temp = idAnalysor('%d'%i,id2)
        IA_temp.query_as_AuId()
        #1+1
        if id2 in IA_temp.RId_list:       
             two_hop_path_list.append([int(id1),i,int(id2)])
        elif id2 in IA_temp.Id_list or id1 in IB.Id_list:
             two_hop_path_list.append([int(id1),i,int(id2)])

        for j in IA_temp.RId_list:
            IA_temp2 = idAnalysor('%d'%j,id2)
            IA_temp2.query_as_AuId()
            #1+1+1
            if id2 in IA_temp2.RId_list:
                three_hop_path_list.append([int(id1),i,j,int(id2)])
            elif id2 in IA_temp2.Id_list or id1 in IB.Id_list:
                three_hop_path_list.append([int(id1),i,j,int(id2)])
        #1+2
        intersection = IA_temp.id_set & IB.id_set
        for j in intersection:
            three_hop_path_list.append([int(id1),i,j,int(id2)])
    #if next=Fid,CId,JId,AfId
    if IA.is_id1_ID():
        if IB.is_id1_ID():#id--id
            IB.query_as_RId()
            for i in IB.Id_list:
                IB_temp=idAnalysor('%d'%i,id1) #search in reverse direction
                IB_temp.query_as_AuId()
                intersection=IA.id_set & IB_temp.id_set
                for j in intersection:
                    three_hop_path_list.append([int(id1),j,i,int(id2)]) 
            else:
                for i in IB.Id_list:#id--AuId
                    IB_temp=idAnalysor('%d'%i,id1) #search in reverse direction
                    IB_temp.query_as_AuId()
                    intersection=IA.id_set & IB_temp.id_set
                    for j in intersection:
                        three_hop_path_list.append([int(id1),j,i,int(id2)]) 
    else:#AuId-AfId-AuId-Id
        for i in IB.AuId_list:
            IB_temp=idAnalysor('%d'%i,id1) #search in reverse direction
            IB_temp.query_as_AuId()
            intersection=set(IA.AfId_list) & set(IB_temp.AfId_list)
            for j in intersection:
                three_hop_path_list.append([int(id1),j,i,int(id2)])  
    return one_hop_path + two_hop_path_list + three_hop_path_list#返回path的list

if __name__ == "__main__":
    id1=2332023333
    id2=2310280492
    print("test")
    start_time = datetime.now()
    result = getPath(id1,id2)
    print(result)
    #print (str(cache.node_set))
    delta = datetime.now() - start_time
    print("\nCost time: %s s"%(str(delta.microseconds/1000)))
    print("\nans count:%d")%len(result)
    
