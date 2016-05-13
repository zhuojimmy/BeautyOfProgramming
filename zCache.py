# -*- coding: utf-8 -*-
#缓存操作直接加在 analysor 查询类里
class zCache:
    def __init__(self):
        #set([id(Au,F,C,J),[Id,[RId],[AuId]])
        self.node_set = set()
    #添加节点    
    def add_node(self, node):
        for i_node in self.node_set:
            if i_node[0] == node[0]:
                return
        self.node_set.add(node)
 
    # 查询节点
    def query_by_id(self, id):
        for i_node in self.node_set:
            if i_node[0] == id:
                return i_node
        else:#查询失败
            return -1 
            