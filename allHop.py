from APIAccess import QueryById, QueryIdByAuId,QueryIdByAuId2, QueryAfIdByAuId, QueryAuIdByAfId, QueryIdByFId, QueryIdByCId, QueryIdByJId, QueryIdByRId, isId
from zCache import zCache
def hop_path(id1,id2):
	#entity = [ id_RId_list, id_AuId_list, id_FId_list, id_JId, id_CId]
	hop_path = []
	is_id1_Id=isId(id1)
	is_id2_Id=isId(id2)
	if is_id1_Id:
		Entity_3=QueryById(id1)
		AuFCJId_list_5=Entity_3[1]+Entity_3[2]
		if(Entity_3[3]!=0):
			AuFCJId_list_5.append(Entity_3[3])
		if(Entity_3[4]!=0):
			AuFCJId_list_5.append(Entity_3[4])
		#Id-Id  Id-AuId
		if int(id2) in Entity_3[0] or int(id2) in Entity_3[1]:
			hop_path.append([int(id1),int(id2)])
		#Id-Id-
		for Id_4 in Entity_3[0]:
			Entity_4=QueryById(Id_4)
			#Id-Id-Id  Id-Id-AuId
			if int(id2) in Entity_4[0] or int(id2) in Entity_4[1]:
					hop_path.append([int(id1),Id_4,int(id2)])
			#Id-Id-Id-(Id,AuId)
			for Id_5 in Entity_4[0]:
				Entity_5=QueryById(Id_5)
				if int(id2) in Entity_5[0] or int(id2) in Entity_5[1]:
					hop_path.append([int(id1),Id_4,Id_5,int(id2)])
			#Id-Id-(AuId,FId,CId,JId)-Id
			if isId(id2):
				Entity_6=QueryById(id2)
				AuFCJId_list_3=Entity_6[1]+Entity_6[2]
				if(Entity_6[3]!=0):
					AuFCJId_list_3.append(Entity_6[3])
				if(Entity_6[4]!=0):
					AuFCJId_list_3.append(Entity_6[4])
				AuFCJId_list_4=Entity_4[1]+Entity_4[2]
				if(Entity_4[3]!=0):
					AuFCJId_list_4.append(Entity_4[3])
				if(Entity_4[4]!=0):
					AuFCJId_list_4.append(Entity_4[4])
				AuFCJId_list_n_2=list(set(AuFCJId_list_3).intersection(set(AuFCJId_list_4)))
				for AuFCJId_2 in AuFCJId_list_n_2:
					hop_path.append([int(id1),Id_4,AuFCJId_2,int(id2)])	
		if is_id2_Id:
			#Id-(AuId,FId,CId,JId)-Id-Id
			Entity_t=QueryIdByRId(id2)
			for i in Entity_t:
				AuFCJId_list_t=i[1]+i[2]
				if(i[3]!=0):
					AuFCJId_list_t.append(i[3])
				if(i[4]!=0):
					AuFCJId_list_t.append(i[4])
				AuFCJId_list_n_t=list(set(AuFCJId_list_5).intersection(set(AuFCJId_list_t)))
				for AuFCJId_t in AuFCJId_list_n_t:
					hop_path.append([int(id1), AuFCJId_t,i[0],int(id2)])
			#Id-(AuId,FId,CId,JId)-Id
			Entity_6=QueryById(id2)
			AuFCJId_list_3=Entity_6[1]+Entity_6[2]
			if(Entity_6[3]!=0):
				AuFCJId_list_3.append(Entity_6[3])
			if(Entity_6[4]!=0):
				AuFCJId_list_3.append(Entity_6[4])
			AuFCJId_list_n_4=list(set(AuFCJId_list_5).intersection(set(AuFCJId_list_3)))
			for AuFCJId_4 in AuFCJId_list_n_4:
					hop_path.append([int(id1),AuFCJId_4,int(id2)])		

		else:
			#Id-AuId-AfId-AuId
			for AuId_2 in Entity_3[1]:
				AfId_list_4=QueryAfIdByAuId(id2)
				AfId_list_5=QueryAfIdByAuId(AuId_2)
				AfId_list_n_3=list(set(AfId_list_4).intersection(set(AfId_list_5)))
				for AfId_4 in AfId_list_n_3:
						hop_path.append([int(id1),AuId_2,AfId_4,int(id2)])
			#Id-(AuId,FId,CId,JId)-Id-AuId
			Entity_7=QueryIdByAuId2(id2)
			for i in Entity_7:
				AuFCJId_list_t=i[1]+i[2]
				if(i[3]!=0):
					AuFCJId_list_t.append(i[3])
				if(i[4]!=0):
					AuFCJId_list_t.append(i[4])
				AuFCJId_list_n_t=list(set(AuFCJId_list_5).intersection(set(AuFCJId_list_t)))
				for AuFCJId_t in AuFCJId_list_n_t:
					hop_path.append([int(id1), AuFCJId_t,i[0],int(id2)])
	else:
		#AuId-AfId-
		AfId_list_1=QueryAfIdByAuId(id1)
		if is_id2_Id:
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

		#AuId-Id-
		Id_list_1=QueryIdByAuId(id1)
		for Id_1 in Id_list_1:
			#AuId-Id
			if int(id2)==Id_1:
				hop_path.append([int(id1),int(id2)])
			Entity_1=QueryById(Id_1)
			if is_id2_Id:
				for Id_3 in Entity_1[0]:
					#AuId-Id-Id
					if int(id2)==Id_3:
						hop_path.append([int(id1),Id_1,int(id2)])
					#AuId-Id-Id-Id
					Id_list_3=QueryById(Id_3)[0]
					if int(id2) in Id_list_3:
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
			else:
				#AuId-Id-AuId
				if int(id2) in Entity_1[1]:
					hop_path.append([int(id1),Id_1,int(id2)])
				#AuId-Id-Id-AuId
				Id_list_2=QueryIdByAuId(id2)
				Id_list_n_1=list(set(Entity_1[0]).intersection(set(Id_list_2)))
				for Id_2 in Id_list_n_1:
					hop_path.append([int(id1),Id_1,Id_2,int(id2)])
	return hop_path
