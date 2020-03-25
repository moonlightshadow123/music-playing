import os, music21

dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, "songs"))

class Parser:
	def __init__(self, song_name):
		self.file_name = os.path.abspath(os.path.join(dir_path, song_name))
		c = music21.converter.parse(self.file_name)
		self.stream = music21.stream.Stream(c)


if __name__ == "__main__":
	p = Parser("test.abc")
