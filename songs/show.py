from music21 import *
c = converter.parse("molihua.abc")
s = stream.Stream(c)
s.show("text")