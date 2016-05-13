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
	return hop_path