from datetime import datetime
import urllib
import json

url_head = "https://oxfordhk.azure-api.net/academic/v1.0/evaluate?"
key_info = "&subscription-key=f7cc29509a8443c5b3a5e56b0e38b5a6"

def  query_api(expr):
        try:
            obj_url = url_head + expr + key_info
            req = urllib.urlopen(obj_url)
            result = req.read()
            #res_json = json.loads(html_result)
            return result
        except Exception as e:
            return("Query exception" + str(e))

def QueryById(Id):
    expr = "expr=Id=%s&count=10000&attributes=Id,AA.AuId,AA.AfId,RId,C.CId,F.FId,J.JId" % Id
    api_return = query_api(expr)
    res_json = json.loads(api_return)
    entity = []
    if "entities" in res_json:
        id_RId_list = []
        id_AuId_list = []
        id_FId_list = []
        id_CId = 0
        id_JId = 0
        if "RId" in res_json["entities"][0]:
            id_RId_list.extend(res_json["entities"][0]["RId"])
        if "AA" in res_json["entities"][0]:
            for j in res_json["entities"][0]["AA"]:
                id_AuId_list.append(j['AuId'])
        if "F" in res_json["entities"][0]:
            for j in res_json["entities"][0]["F"]:
                id_FId_list.append(j["FId"])
        if "J" in res_json["entities"][0]:
            id_JId=res_json["entities"][0]["J"]["JId"]
        if "C" in res_json["entities"][0]:
            id_CId=res_json["entities"][0]["C"]["CId"]
        entity = [ id_RId_list, id_AuId_list, id_FId_list, id_JId, id_CId]
    return entity

def QueryAfIdByAuId(AuId):
    expr = "expr=composite(AA.AuId=%s)&count=10000&attributes=Id,AA.AuId,AA.AfId" % AuId
    api_return = query_api(expr)
    res_json = json.loads(api_return)
    AfId_list = []
    if "entities" in res_json:
        for i in res_json["entities"]:
            if "AA" in i:
                for j in i["AA"]:
                    if int(AuId)==j["AuId"] and "AfId" in j:
                        if j["AfId"] not in AfId_list :
                            AfId_list.append(j["AfId"])
    return AfId_list

def QueryIdByAuId(AuId):
    expr = "expr=composite(AA.AuId=%s)&count=10000&attributes=Id" % AuId
    api_return = query_api(expr)
    res_json = json.loads(api_return)
    Id_list = []
    if "entities" in res_json:
        for i in res_json["entities"]:
            Id_list.append(i["Id"])
    return Id_list

def QueryRIdByAuId(AuId):
    #result=[[Id,[RId_list]],[],...[]]
    expr = "expr=composite(AA.AuId=%s)&count=10000&attributes=Id" % AuId
    api_return = query_api(expr)
    res_json = json.loads(api_return)
    result = []
    if "entities" in res_json:
        for i in res_json["entities"]:
            if "RId" in res_json["entities"][0]:
                RId_list_by_AuId.extend(i["RId"])
            Entity_by_AuId=[i["Id"],RId_list_by_AuId]
            result.append(Entity_by_AuId)
    return result

def QueryRIdByFId(FId):
    #result=[[Id,[RId_list]],[],...[]]
    expr = "expr=composite(F.FId=%s)&count=10000&attributes=Id" % FId
    api_return = query_api(expr)
    res_json = json.loads(api_return)
    result = []
    if "entities" in res_json:
        for i in res_json["entities"]:
            if "RId" in res_json["entities"][0]:
                RId_list_by_AuId.extend(i["RId"])
            Entity_by_AuId=[i["Id"],RId_list_by_AuId]
            result.append(Entity_by_AuId)
    return result

def QueryRIdByCId(CId):
    #result=[[Id,[RId_list]],[],...[]]
    expr = "expr=composite(C.CId=%s)&count=10000&attributes=Id" % CId
    api_return = query_api(expr)
    res_json = json.loads(api_return)
    result = []
    if "entities" in res_json:
        for i in res_json["entities"]:
            if "RId" in res_json["entities"][0]:
                RId_list_by_AuId.extend(i["RId"])
            Entity_by_AuId=[i["Id"],RId_list_by_AuId]
            result.append(Entity_by_AuId)
    return result

def QueryRIdByJId(JId):
    #result=[[Id,[RId_list]],[],...[]]
    expr = "expr=composite(J.JId=%s)&count=10000&attributes=Id" % JId
    api_return = query_api(expr)
    res_json = json.loads(api_return)
    result = []
    if "entities" in res_json:
        for i in res_json["entities"]:
            if "RId" in res_json["entities"][0]:
                RId_list_by_AuId.extend(i["RId"])
            Entity_by_AuId=[i["Id"],RId_list_by_AuId]
            result.append(Entity_by_AuId)
    return result

def QueryAuIdByAfId(AfId):
    expr = "expr=composite(AA.AfId=%s)&count=10000&attributes=Id,AA.AuId,AA.AfId" % AfId
    api_return = query_api(expr)
    res_json = json.loads(api_return)
    AuId_list = []
    if "entities" in res_json:
        for i in res_json["entities"]:
            if "AA" in i:
                for j in i["AA"]:
                    if "AfId" in j:
                        if(int(AfId)==j["AfId"]):
                            if(j["AuId"] not in AuId_list):
                                AuId_list.append(j["AuId"])
    return AuId_list

def QueryIdByFId(FId):
    expr = "expr=composite(F.FId=%s)&count=1000&attributes=Id" % FId
    api_return = query_api(expr)
    res_json = json.loads(api_return)
    Id_list = []
    if "entities" in res_json:
        for i in res_json["entities"]:
            Id_list.append(i['Id'])
    return Id_list

def QueryIdByCId(CId):
    expr = "expr=composite(C.CId=%s)&count=1000&attributes=Id" % CId
    api_return = query_api(expr)
    res_json = json.loads(api_return)
    Id_list = []
    if "entities" in res_json:
        for i in res_json["entities"]:
            Id_list.append(i['Id'])
    return Id_list

def QueryIdByJId(JId):
    expr = "expr=composite(J.JId=%s)&count=1000&attributes=Id" % JId
    api_return = query_api(expr)
    res_json = json.loads(api_return)
    Id_list = []
    if "entities" in res_json:
        for i in res_json["entities"]:
            Id_list.append(i['Id'])
    return Id_list

def isId(id):
    expr = "expr=Id=%s&count=10000&attributes=Id,AA.AuId,AA.AfId,RId,C.CId,F.FId,J.JId" % id
    api_return = query_api(expr)
    res_json = json.loads(api_return)
    if "entities" in res_json:
        if "AA" in res_json["entities"][0]:
           return True
        else:
            return False
