import os, music21
from utils import getAcc, NStrToVStr, qlenToDur, minusToB

dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, "songs"))

class Parser:
	def __init__(self, song_name):
		self.file_name = os.path.abspath(os.path.join(dir_path, song_name))
		c = music21.converter.parse(self.file_name)
		self.stream = music21.stream.Stream(c)
		self.tre_iter = iter(self.stream[1])
		self.bas_iter = iter(self.stream[2])
		self.measure = "4/4"
		self.key = "C"
		self.speed = 88

	def getNextTre(self):
		m = None
		try: m = next(self.tre_iter)
		except: print("No Tre Next!")
		return m

	def getNextBas(self):
		m = None
		try: m = next(self.bas_iter)
		except: print("No Bas Next!")
		return m

	def mToData(self, measure):
		res = []
		if not measure: return res
		m_offset = measure.offset
		for notes in measure.notesAndRests:
			cur_notes = []
			if type(notes) == music21.note.Note:
				# print("bingo")
				# print(notes.pitch)
				# print(notes.duration.type)
				# print(notes)
				cur_notes.append(self.nToData(notes, m_offset))
			if type(notes) == music21.chord.Chord:
				# print("hello")
				for note in notes.notes:
					cur_notes.append(self.nToData(note, m_offset))
			if type(notes) == music21.note.Rest:
				# print("nihao")
				cur_notes.append(self.rToData(notes, m_offset))
			res.append(cur_notes)
		return res

	def nToData(self, note, m_offset):
		res = []
		if not note: return res
		nstr = minusToB(note.nameWithOctave)
		res.append(NStrToVStr(nstr))
		res.append(getAcc(nstr))
		res.append(qlenToDur(note.duration.quarterLength))
		res.append(note.offset + m_offset)
		res.append(note.offset + m_offset + note.duration.quarterLength)
		return res

	def rToData(self, rest, m_offset):
		res = []
		if not rest: return res
		vstr = "c/4"
		res.append(vstr)
		res.append("")
		res.append(qlenToDur(rest.duration.quarterLength) + "r")
		res.append(rest.offset + m_offset)
		res.append(rest.offset + m_offset + rest.duration.quarterLength)
		return res

	def getNext(self):
		tre_m1 = self.getNextTre()
		tre_m2 = self.getNextTre()
		bas_m1 = self.getNextBas()
		bas_m2 = self.getNextBas()
		data = {"tre_notes_raw":[], "bas_notes_raw":[]}
		'''
		data["tre_notes_raw"].append(self.mToData(tre_m1))
		data["tre_notes_raw"].append(self.mToData(tre_m2))
		data["bas_notes_raw"].append(self.mToData(bas_m1))
		data["bas_notes_raw"].append(self.mToData(bas_m2))
		'''
		data["tre_notes_raw"] = self.mToData(tre_m1) + ['|']
		data["tre_notes_raw"] += self.mToData(tre_m2)
		data["bas_notes_raw"] = self.mToData(bas_m1) + ['|']
		data["bas_notes_raw"] += self.mToData(bas_m2)
		# return (data, (tre_m1 != None and tre_m2 != None and bas_m1 != None and bas_m2 != None))
		return data

if __name__ == "__main__":
	p = Parser("test1.abc")
	for i in range(10):
		print(p.getNext())
		# print(p.getNext())
		# print(p.getNextBas())
