#-*- coding:utf-8 -*-
#答案返回结果整合
import urllib
import json
import oneHop
import twoHop
import threeHop

def getResult(id1,id2):
    #allPath = oneHop.getPath(id1,id2) + twoHop.getPath(id1,id2) + threeHop.getPath(id1,id2)
    #return str(allPath)
    return str(twoHop.getPath(id1,id2))
    
# test url : http://localhost/?id1=2147152072&id2=189831743