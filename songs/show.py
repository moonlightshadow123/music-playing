from music21 import *
c = converter.parse("test2.abc")
s = stream.Stream(c)
s.show()