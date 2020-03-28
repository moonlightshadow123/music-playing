import pyOSC3
import threading
from config import config
from utils import NIdxToFreq

class OSC:
	def __init__(self):
		ip, port = config["ip"], config["port"]
		self.lock = threading.Lock()
		self.client = pyOSC3.OSCClient()
		self.client.connect((ip, port))

	def noteOn(self, NIdx):
		msg = pyOSC3.OSCMessage()
		msg.setAddress("/noteOn")
		msg.append(NIdx)
		freq = NIdxToFreq(NIdx)
		# print(freq)
		msg.append(freq)
		with self.lock:
			self.client.send(msg)

	def noteOff(self, NIdx):
		msg = pyOSC3.OSCMessage()
		msg.setAddress("/noteOff")
		msg.append(NIdx)
		with self.lock:
			self.client.send(msg)

	def clear(self):
		msg = pyOSC3.OSCMessage()
		msg.setAddress("/clear")
		with self.lock:
			self.client.send(msg)

if __name__ == "__main__":
	o = OSC()
	o.noteOff(60)