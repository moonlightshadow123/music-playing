import pickle

config = {
"ip":"127.0.0.1",
"port": 57120,
"amp": 0.8,
"decay": 0.6,
}

noteIdx_noteStr = None
with open("../data/noteIdx_noteStr.pkl", "rb") as f:
	noteIdx_noteStr = pickle.load(f)

btnIdx_noteIdx = None
with open("../data/btnIdx_noteIdx.pkl", "rb") as f:
	btnIdx_noteIdx = pickle.load(f)

btnNum_btnIdx = None
with open("../data/btnNum_btnIdx.pkl", "rb") as f:
	btnNum_btnIdx = pickle.load(f)

noteStr_noteIdx = None
with open("../data/noteStr_noteIdx.pkl", "rb") as f:
	noteStr_noteIdx = pickle.load(f)

if __name__ == "__main__":
	print(config)
	print(noteIdx_noteStr)
	print(btnIdx_noteIdx)
	print(btnNum_btnIdx)