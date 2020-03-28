import collections
import numpy as np
import time

from config import noteStr_noteIdx

def wait_until(somepredicate, timeout, period=0.1, *args, **kwargs):
    mustend = time.time() + timeout
    while time.time() < mustend:
        if somepredicate(*args, **kwargs): return True
        time.sleep(period)
        print("sleeping")
    return False

def getAcc(noteStr):
    acc = noteStr[1:-1]
    if acc: 
        return acc
    else: 
        return ""

def NStrToVStr(noteStr):
    noteStr = noteStr.lower()
    noteStr = noteStr[:-1] + "/" +noteStr[-1]
    return noteStr

def VStrToNStr(vexStr):
    vexStr = vexStr.replace("/", "")
    vexStr = vexStr[0].upper() + vexStr[1:]
    return vexStr

def VStrToNIdx(vexStr):
    NStr = VStrToNStr(vexStr)
    return noteStr_noteIdx.get(NStr, -1)


def minusToB(string):
	 return string.replace('-','b')

def qlenToDur(num):
    print(num)
    return str(int(4/num))

def addToSet(cur_set, cur_data,sub_idx=0):
    for each in cur_data:
        cur_set.add(each[sub_idx])

def merge2list(data1, data2, key_func, res_func, append_func, skip = set()):
    res = []
    idx1, idx2 = 0, 0
    cur_key = -1
    while idx1 < len(data1) and idx2 < len(data2):
        cur_set1, cur_set2 = set(), set()
        cur_ele1, cur_ele2 = data1[idx1], data2[idx2]
        # print(cur_ele1)
        # print(cur_ele2)
        if skip and  isinstance(cur_ele1, collections.Hashable) and cur_ele1 in skip:
            idx1 += 1; continue
        if skip and isinstance(cur_ele2, collections.Hashable) and cur_ele2 in skip:
            idx2 += 1; continue
        key1 = key_func(cur_ele1); key2 = key_func(cur_ele2)
        if key1 <= key2:
            res_func(cur_set1, cur_ele1)
            cur_key = key1
            idx1 += 1
        if key1 >= key2:
            res_func(cur_set2, cur_ele2)
            cur_key = key2
            idx2 += 1
        # print(res, cur_key, cur_set1, cur_set2)
        append_func(res, cur_key, cur_set1, cur_set2)
        # res.append((cur_set, cur_key))
    while idx1 < len(data1):
        cur_set1 = set()
        if skip and isinstance(data1[idx1], collections.Hashable) and data1[idx1] in skip:
            idx1 += 1; continue
        res_func(cur_set1, data1[idx1])
        append_func(res, key_func(data1[idx1]), cur_set1, set())
        # res.append((cur_set, key_func(data1[idx1])))
        idx1 += 1
        
    while idx2 < len(data2):
        cur_set2 = set()
        if skip and  isinstance(data2[idx2], collections.Hashable) and data2[idx2] in skip:
            idx2 += 1; continue
        res_func(cur_set2, data2[idx2])
        append_func(res, key_func(data2[idx2]), set(), cur_set2)
        # res.append((cur_set, key_func(data2[idx2])))
        idx2 += 1
        
    return res


def NIdxToFreq(NIdx):
    return 27.5*np.power(2, (NIdx-21)/12)

