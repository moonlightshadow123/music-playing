import pickle


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
'''

with open("btnNum_btnIdx.pkl", "rb") as f:
    btnNum_btnIdx = pickle.load(f)
    for each in btnNum_btnIdx.items():
    	print(each)
    print(len(btnNum_btnIdx.items()))
''' 