﻿# -*- coding: utf-8 -*-
#缓存操作直接加在 analysor 查询类里
class pathCache:
    def __init__(self):
        self.node_set = set()
    #添加节点    
    def add_node(self, node):
        for i_node in self.node_set:
            if i_node.id1 == id:
                return
        self.node_set.add(node)
 
    # 查询节点
    def query_by_id(self, id):
        for i_node in self.node_set:
            if i_node.id1 == id:
                return i_node
        else:#查询失败
            return -1 
            
            
            
if __name__ == "__main__":
    cache = pathCache()
    cache.add_node(1,[1,2,3,4,5])
    print cache.query_by_ID(1)