#-*- coding:utf-8 -*-
"""
The given pair of entity identifiers could be 
[Id, Id], [Id, AA.AuId], [AA.AuId, Id], [AA.AuId, AA.AuId]. 
Each node of a path should be one of the following identifiers: 
Id, F.Fid, J.JId, C.CId, AA.AuId, AA.AfId. 

//����  0509
���������� is_id1_ID()�������ǰid1��ID������ΪTrue������ΪFalse
�������������
ͬ��Id�ڲ�ͬ�������Ϊauid��id���·��ʵĽ��
https://oxfordhk.azure-api.net/academic/v1.0/evaluate?expr=Id=621499171&count=10000&attributes=Id,AA.AuId,AA.AfId,C.CId&subscription-key=f7cc29509a8443c5b3a5e56b0e38b5a6
https://oxfordhk.azure-api.net/academic/v1.0/evaluate?expr=composite(AA.AuId=2140251882)&count=10000&attributes=Id,AA.AuId,AA.AfId,C.CId&subscription-key=f7cc29509a8443c5b3a5e56b0e38b5a6
https://oxfordhk.azure-api.net/academic/v1.0/evaluate?expr=Id=621499171&count=10000&attributes=Id,AA.AuId,AA.AfId,C.CId&subscription-key=f7cc29509a8443c5b3a5e56b0e38b5a6
https://oxfordhk.azure-api.net/academic/v1.0/evaluate?expr=composite(AA.AuId=2140251882)&count=10000&attributes=Id,AA.AuId,AA.AfId,C.CId&subscription-key=f7cc29509a8443c5b3a5e56b0e38b5a6
*//

"""
from datetime import datetime
import urllib
import json

url_head = "https://oxfordhk.azure-api.net/academic/v1.0/evaluate?"
key_info = "&subscription-key=f7cc29509a8443c5b3a5e56b0e38b5a6"


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
#����������ѯ��������ID����Ϊһ������  id_set,���������ڽڵ�id���ϣ���Ϊ���β�ѯ���մ����Ĳ���        
    def id_union(self):
        list_sum = self.AuId_list + self.CId_list +self.JId_list +self.AfId_list +self.FId_list#delete the RId list, it is not a node
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
        global COUNT 
        expr = "expr=composite(AA.AuId=%s)&count=%d&attributes=Id,AA.AfId"%(self.id1,COUNT)
        api_return = query_api(expr)
        res_json = json.loads(api_return)
        #id1��AuId
        if len(res_json["entities"])>0:
            self.id_or_AuId = 1
            for i in res_json["entities"]:
                self.Id_list.append(i['Id'])               
                if "AA" in i:
                    for author in i["AA"]:
                        if "AfId" in author:
                            self.AfId_list.append(author["AfId"])
                       # if "AuId" in author:
                         #   self.AuId_list.append(author["AuId"]) 
            self.id_union()  
        #id1����AuId   
        else:
                self.id_or_AuId = 0
                self.query_as_Id()



    def is_id1_ID(self):
        if self.id_or_AuId == 0:
            return True
        else:
            return False
                
                
#�����ѯ������api�������ı�
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
    #����
    one_hop_path = []
    if id2 in IA.RId_list:
        one_hop_path = [[id1,id2]]
    #����
    two_hop_path_list = []
    intersection = IA.id_set & IB.id_set
    for i in intersection:
        two_hop_path_list.append([int(id1),i,int(id2)])

    #1+1 or 1+2  or 1+1+1
    COUNT= 100
    three_hop_path_list = []
   #if next=Id,AuId
    if IA.is_id1_ID():
        next_set = set(IA.RId_list+IA.AuId_list)
    else:
        next_set = set(IA.RId_list)      
    for i in next_set:
        IA_temp = idAnalysor('%d'%i,id2)
        IA_temp.query_as_AuId()
        if id2 in IA_temp.RId_list:
            #i+1
             two_hop_path_list.append([int(id1),i,int(id2)])
        for j in IA_temp.RId_list:
            IA_temp2 = idAnalysor('%d'%j,id2)
            IA_temp2.query_as_AuId()
            if id2 in IA_temp2.RId_list:
                #1+1+1
                three_hop_path_list.append([int(id1),i,j,int(id2)])
        #1+2
        intersection = IA_temp.id_set & IB.id_set
        for j in intersection:
            three_hop_path_list.append([int(id1),i,j,int(id2)])
    #if next=Fid,CId,JId
    if IA.is_id1_ID():
        for i in IB.RId_list:
            IB_temp=idAnalysor('%d'%i,id1) #search in reverse direction
            IB_temp.query_as_AuId()
            intersection=IA.id_set & IB_temp.id_set
            for j in intersection:
                three_hop_path_list.append([int(id1),j,i,int(id2)])   
    else:
        for i in IB.AuId_list:
            IB_temp=idAnalysor('%d'%i,id1) #search in reverse direction
            IB_temp.query_as_AuId()
            intersection=set(IA.AfId_list) & set(IB_temp.AfId_list)
            for j in intersection:
                three_hop_path_list.append([int(id1),j,i,int(id2)])  
    return one_hop_path + two_hop_path_list + three_hop_path_list#����path��list
'''    
#Ps ѧ�����˼�򲻸�ɾ
    if isId1==1 and isId2==1:
        intersection = id_set_A1 & id_set_B1
        two_hop_path_list = []
        for i in intersection:
	    two_hop_path_list.append([int(id1),i,int(id2)])
	#���ﻹӦ���д���RId�����
    elif isId1==1 and isId2==0:
	for i in IA.RId_list:
	    #��ѯ��Ӧ��AuId
	    pass
    elif isId1==0 and isId2==1:
        for i in IB.RId_list:
	    #��ѯ��Ӧ��AuId
	    pass
    else:
        intersection = id_set_A1 & id_set_B1#��Id��·��
        two_hop_path_list = []
        for i in intersection:
	    two_hop_path_list.append([int(id1),i,int(id2)])
	intersection = id_set_A2 & id_set_B2#��AfId��·��
	for i in intersection:
	    two_hop_path_list.append([int(id1),i,int(id2)])    
    return two_hop_path_list
 '''
if __name__ == "__main__":
    id1=2147152072
    id2=189831743
    print("test")
    start_time = datetime.now()
    result = getPath(id1,id2)
    print(result)
    delta = datetime.now() - start_time
    print("\nCost time: %s ms"%(str(delta.microseconds/1000)))
    print("\nans count:%d")%len(result)
    