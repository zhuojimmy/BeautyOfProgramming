from APIAccess import QueryById, QueryIdByAuId, QueryAfIdByAuId, QueryAuIdByAfId, QueryIdByFId, QueryIdByCId, QueryIdByJId, isId
from zCache import zCache
def hop_path(id1,id2):
	#entity = [ id_RId_list, id_AuId_list, id_FId_list, id_JId, id_CId]
	hop_path = []
	if isId(id1):
		print isId(id1)
	else:
		#AuId-AfId
		AfId_list_1=QueryAfIdByAuId(id1)
		if isId(id2):
			AuId_list_1=QueryById(id2)[1]
			for AuId_1 in AuId_list_1:
				AfId_list_2=QueryAfIdByAuId(AuId_1)
				AfId_list_n_1=list(set(AfId_list_1).intersection(set(AfId_list_2)))
				for AfId_2 in AfId_list_n_1:
					hop_path.append([int(id1),AfId_2,AuId_1,int(id2)])
		else:
			AfId_list_3=QueryAfIdByAuId(id2)
			AfId_list_n_2=list(set(AfId_list_1).intersection(set(AfId_list_3)))
			for AfId_3 in AfId_list_n_2:
					hop_path.append([int(id1),AfId_3,int(id2)])

		#AuId-Id
		Id_list_1=QueryIdByAuId(id1)
		for Id_1 in Id_list_1:
			Entity_1=QueryById(Id_1)
			if isId(id2):
				#AuId-Id-Id-Id
				for Id_3 in Entity_1[0]:
					Id_list_3=QueryById(Id_3)[0]
					if id2 in Id_list_3:
						hop_path.append([int(id1),Id_1,Id_3,int(id2)])
				#AuId-Id-(AuId,FId,CId,JId)-Id
				Entity_2=QueryById(id2)
				AuFCJId_list_1=Entity_1[1]+Entity_1[2]
				if(Entity_1[3]!=0):
					AuFCJId_list_1.append(Entity_1[3])
				if(Entity_1[4]!=0):
					AuFCJId_list_1.append(Entity_1[4])
				AuFCJId_list_2=Entity_2[1]+Entity_2[2]
				if(Entity_2[3]!=0):
					AuFCJId_list_2.append(Entity_2[3])
				if(Entity_2[4]!=0):
					AuFCJId_list_2.append(Entity_2[4])
				AuFCJId_list_n_1=list(set(AuFCJId_list_1).intersection(set(AuFCJId_list_2)))
				for AuFCJId_1 in AuFCJId_list_n_1:
					hop_path.append([int(id1),Id_1,AuFCJId_1,int(id2)])
					print AuFCJId_1
			else:
				#AuId-Id-Id-AuId
				Id_list_2=QueryIdByAuId(id2)
				Id_list_n_1=list(set(Entity_1[0]).intersection(set(Id_list_2)))
				for Id_2 in Id_list_n_1:
					hop_path.append([int(id1),Id_1,Id_2,int(id2)])
	return hop_path