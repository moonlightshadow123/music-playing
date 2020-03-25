from pythonosc import udp_client
import pyOSC3
import threading
from config import config

class NoteClient:
	def __init__(self):
		ip, port = config["ip"], config["port"]
		self.lock = threading.Lock()
		self.client = pyOSC3.OSCClient()
		self.client.connect((ip, port))
		self.onDict = {} # key -- (note, amp, decay)
		self.sharp = False
		self.flat = False

	def noteOn(self, key, note):
		print("Note on!!")
		msg = pyOSC3.OSCMessage()
		msg.setAddress("/noteOn")
		from config import config
		amp, decay = config["amp"], config["decay"]
		msg.append(note)
		msg.append(amp)
		msg.append(decay)
		with self.lock:
			self.client.send(msg)
			if self.sharp: note += 1
			if self.flat: note -= 1
			self.onDict[key] = (note, amp, decay)

	def noteOff(self, key):
		print("Note off!!")
		with self.lock:
			pair = self.onDict.get(key)
			if not pair:
				return
			(note, amp, decay) = pair
		msg = pyOSC3.OSCMessage()
		msg.setAddress("/noteOff")
		msg.append(note)
		msg.append(amp)
		msg.append(decay)
		with self.lock:
			self.client.send(msg)
			if self.onDict.get(key):
				del self.onDict[key]

	def sharpOn(self):
		with self.lock:
			self.sharp = True

	def sharpOff(self):
		with self.lock:
			self.sharp = False

	def flatOn(self):
		with self.lock:
			self.flat = True

	def faltOff(self):
		with self.lock:
			self.flat = False
