#-*- coding:utf-8 -*-
#答案返回结果整合
import urllib
import json
import oneHop
import newTwoHop
import threeHop


def getResult(id1,id2):
    #allPath = oneHop.getPath(id1,id2) + twoHop.getPath(id1,id2) + threeHop.getPath(id1,id2)
    #return str(allPath)
    #twoHop.getPath(id1,id2) 
    return oneHop.one_hop_path(id1,id2)+newTwoHop.two_hop_path(id1,id2)#+threeHop.three_hop_path(id1,id2)
    #最终返回list
    
# test url : http://localhost/?id1=2147152072&id2=189831743