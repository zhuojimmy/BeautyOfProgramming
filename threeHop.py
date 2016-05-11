#Zhuo Qinzheng 0511
from oneHop import QueryById, QueryIdByAuId, QueryAfIdByAuId, QueryAuIdByAfId, QueryIdByFId, QueryIdByCId, QueryIdByJId, isId

def three_hop_path(id1,id2):
    #entity = [ id_RId_list, id_AuId_list, id_FId_list, id_JId, id_CId]
    three_hop_path = []
    if(isId(id1)):
        RIdById_list=QueryById(id1)[0]
        for tempId in RIdById_list:
            RIdById_list=QueryById(tempId)[0]
            for Id in RIdById_list:
                IdAuIdById_list=QueryById(Id)[0]+QueryById(Id)[1]
                if(int(id2) in IdAuIdById_list):
                    three_hop_path.append([int(id1),tempId,Id,int(id2)])
            AuIdById_list=QueryById(tempId)[1]
            for tempAuId in AuIdById_list:
                Id_list=QueryIdByAuId(tempAuId)
                if(int(id2) in Id_list):
                    three_hop_path.append([int(id1),tempId,tempAuId,int(id2)])
            FIdById_list=QueryById(tempId)[2]
            for tempFId in FIdById_list:
                Id_list=QueryIdByFId(tempFId)
                if(int(id2) in Id_list):
                    three_hop_path.append([int(id1),tempId,tempFId,int(id2)])
            JIdById=QueryById(tempId)[3]
            Id_list=QueryIdByJId(JIdById)
            if(int(id2) in Id_list):
                three_hop_path.append([int(id1),tempId,JIdById,int(id2)])   
            CIdById=QueryById(tempId)[4]
            Id_list=QueryIdByCId(CIdById)
            if(int(id2) in Id_list):
                three_hop_path.append([int(id1),tempId,CIdById,int(id2)])  

        AuIdById_list=QueryById(id1)[1]
        for tempAuId in AuIdById_list:
            IdByAuId_list=QueryIdByAuId(tempAuId)
            for tempId in IdByAuId_list:
                IdAuIdById_list=QueryById(tempId)[0]+QueryById(tempId)[1]
                if(int(id2) in IdAuIdById_list):
                    three_hop_path.append([int(id1),tempAuId,tempId,int(id2)])
            AfIdByAuId_list=QueryAfIdByAuId(tempAuId)
            for tempAfId in AfIdByAuId_list:
                AuIdByAfId_list=QueryAuIdByAfId(tempAfId)
                if(int(id2) in AuIdByAfId_list):
                    three_hop_path.append([int(id1),tempAuId,tempAfId,int(id2)])

        FIdById_list=QueryById(id1)[2]
        for tempFId in FIdById_list:
            Id_list=QueryIdByFId(tempFId)
            for TempId in Id_list:
                IdAuIdById_list=QueryById(TempId)[0]+QueryById(TempId)[1]
                if(int(id2) in IdAuIdById_list):
                    three_hop_path = [[int(id1),tempFId,TempId,int(id2)]]
        JIdById=QueryById(id1)[3]
        Id_list=QueryIdByJId(JIdById)
        for TempId in Id_list:
                IdAuIdById_list=QueryById(TempId)[0]+QueryById(TempId)[1]
                if(int(id2) in IdAuIdById_list):
                    three_hop_path = [[int(id1),JIdById,TempId,int(id2)]]
        CIdById=QueryById(id1)[4]
        Id_list=QueryIdByCId(CIdById)
        for TempId in Id_list:
                IdAuIdById_list=QueryById(TempId)[0]+QueryById(TempId)[1]
                if(int(id2) in IdAuIdById_list):
                    three_hop_path = [[int(id1),CIdById,TempId,int(id2)]]

    else:
        IdByAuId_list=QueryIdByAuId(id1)
        for tempId in IdByAuId_list:
            RIdById_list=QueryById(tempId)[0]
            for Id in RIdById_list:
                IdAuIdById_list=QueryById(Id)[0]+QueryById(Id)[1]
                if(int(id2) in IdAuIdById_list):
                    three_hop_path.append([int(id1),tempId,Id,int(id2)])
            AuIdById_list=QueryById(tempId)[1]
            for tempAuId in AuIdById_list:
                Id_list=QueryIdByAuId(tempAuId)
                if(int(id2) in Id_list):
                    three_hop_path.append([int(id1),tempId,tempAuId,int(id2)])
            FIdById_list=QueryById(tempId)[2]
            for tempFId in FIdById_list:
                Id_list=QueryIdByFId(tempFId)
                if(int(id2) in Id_list):
                    three_hop_path.append([int(id1),tempId,tempFId,int(id2)])
            JIdById=QueryById(tempId)[3]
            Id_list=QueryIdByJId(JIdById)
            if(int(id2) in Id_list):
                three_hop_path.append([int(id1),tempId,JIdById,int(id2)])   
            CIdById=QueryById(tempId)[4]
            Id_list=QueryIdByCId(CIdById)
            if(int(id2) in Id_list):
                three_hop_path.append([int(id1),tempId,CIdById,int(id2)])  

        AfIdByAuId_list=QueryAfIdByAuId(id2)
        for tempAfId in AfIdByAuId_list:
            AuIdByAfId_list=QueryAuIdByAfId(tempAfId)
            for AuId in AuIdByAfId_list:
                IdByAuId_list=QueryIdByAuId(AuId)
                if (int(id2) in IdByAuId_list):
                   three_hop_path = [[int(id1),tempAfId,AuId,int(id2)]]
                
    return three_hop_path
