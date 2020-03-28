from music21 import *
c = converter.parse("test1.abc")
s = stream.Stream(c)
s.show("text")