#Zhuo Qinzheng 0511
from oneHop import QueryById, QueryIdByAuId, QueryAfIdByAuId, QueryAuIdByAfId, QueryIdByFId, QueryIdByCId, QueryIdByJId, isId

def two_hop_path(id1,id2):
    #entity = [ id_RId_list, id_AuId_list, id_FId_list, id_JId, id_CId]
    two_hop_path = []
    if(isId(id1)):
        RIdById_list=QueryById(id1)[0]
        for tempId in RIdById_list:
            IdAuIdById_list=QueryById(tempId)[0]+QueryById(tempId)[1]
            if(int(id2) in IdAuIdById_list):
                two_hop_path.append([int(id1),tempId,int(id2)])
        AuIdById_list=QueryById(id1)[1]
        for tempAuId in AuIdById_list:
            Id_list=QueryIdByAuId(tempAuId)
            if(int(id2) in Id_list):
                two_hop_path.append([int(id1),tempAuId,int(id2)])
        FIdById_list=QueryById(id1)[2]
        for tempFId in FIdById_list:
            Id_list=QueryIdByFId(tempFId)
            if(int(id2) in Id_list):
                two_hop_path.append([int(id1),tempFId,int(id2)])
        JIdById=QueryById(id1)[3]
        Id_list=QueryIdByJId(JIdById)
        if(int(id2) in Id_list):
            two_hop_path.append([int(id1),JIdById,int(id2)])   
        CIdById=QueryById(id1)[4]
        Id_list=QueryIdByCId(CIdById)
        if(int(id2) in Id_list):
            two_hop_path.append([int(id1),CIdById,int(id2)])  

    else:
        IdByAuId_list=QueryIdByAuId(id1)
        for tempId in IdByAuId_list:
            IdAuIdById_list=QueryById(tempId)[0]+QueryById(tempId)[1]
            if(int(id2) in IdAuIdById_list):
                two_hop_path.append([int(id1),tempId,int(id2)])
        AfIdByAuId_list=QueryAfIdByAuId(id1)
        for tempAfId in AfIdByAuId_list:
            AuIdByAfId_list=QueryAuIdByAfId(tempAfId)
            if(int(id2) in AuIdByAfId_list):
                two_hop_path.append([int(id1),tempAfId,int(id2)])

    return two_hop_path
