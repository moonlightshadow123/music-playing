import pickle
import json
'''
key_list = []
with open("key_list.res.pkl", "rb") as f:
    key_list = pickle.load(f)

print(len(key_list))

key_list[18] = -1
key_list[93] = -2

btnNum_btnIdx = {}

for idx, btnNum in enumerate(key_list):
	btnNum_btnIdx[btnNum] = idx

with open("btnNum_btnIdx.pkl", "wb") as f:
	pickle.dump(btnNum_btnIdx, f)


with open("btnNum_btnIdx.pkl", "rb") as f:
    btnNum_btnIdx = pickle.load(f)
    for each in btnNum_btnIdx.items():
    	print(each)
    print(len(btnNum_btnIdx.items()))
''' 
"""
with open("noteIdx_noteStr.json", "r") as f:
	jsonStr = f.read()#.replace("\n", "")
	print(jsonStr)
	a = json.loads(jsonStr)
	print(a)

	res = {} 
	for key,val in a.items():
		res[int(key)] = val
	with open("noteIdx_noteStr.pkl", "wb") as pkl:
		pickle.dump(res, pkl)

"""
"""
with open("btnIdx_noteIdx.json", "r") as f:
	jsonStr = f.read()#.replace("\n", "")
	print(jsonStr)
	a = json.loads(jsonStr)
	print(a)

	res = {} 
	for key,val in a.items():
		res[int(key)] = int(val)
	with open("btnIdx_noteIdx.pkl", "wb") as pkl:
		pickle.dump(res, pkl)
"""
with open("noteIdx_noteStr.pkl", "rb") as f:
    noteIdx_noteStr = pickle.load(f)
    noteStr_noteIdx = {}
    for key,val in noteIdx_noteStr.items():
    	for eachStr in val: 
    		noteStr_noteIdx[eachStr] = key
    with open("noteStr_noteIdx.pkl", "wb") as res_f:
    	pickle.dump(noteStr_noteIdx, res_f)