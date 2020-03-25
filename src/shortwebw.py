from PyQt5.QtWidgets import QApplication, QPushButton, QWidget, QSizePolicy, QGridLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView

from PyQt5.QtCore import QObject,  QUrl,  QRect

import os, time

def getAcc(note):
  acc = note[1:-1]
  if acc: 
    return acc
  else: 
    return ""

def convNote(note):
   note = note.lower()
   note = note[:-1] + "/" +note[-1]
   return note

class ShortWebW(QWidget):
  def __init__(self):
    super(ShortWebW, self).__init__()
    self.grid = QGridLayout(self)
    self.view_list = [ShortWebView(), ShortWebView()]
    self.view_list[0].setSizePolicy(QSizePolicy.MinimumExpanding,QSizePolicy.Preferred)
    self.view_list[1].setSizePolicy(QSizePolicy.MinimumExpanding,QSizePolicy.Preferred)
    self.grid.addWidget(self.view_list[0], 0,0,1,1)
    self.grid.addWidget(self.view_list[1], 1,0,1,1)
    self.setFixedWidth(300)
    self.setFixedHeight(700)   

class ShortWebView(QWebEngineView):

    def __init__(self, *args, **kwargs):
        super(ShortWebView, self).__init__(*args, **kwargs)
        self.file_name = "shortweb.html"

        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir,"web", self.file_name))
        local_url = QUrl.fromLocalFile(file_path)
        self.load(local_url)

    def drawNote(self, key, note, clef, duration="q"):
        data = {"btnNum":str(key), "note":convNote(note), "duration":duration, "acc":getAcc(note), "clef":clef}
        #js_string = r'staff.drawNote({"key":'+str(key)+', "note":["'+convNote(note)+'"], "duration":"'+duration+'"});'
        js_string = r"draw_note(" + str(data) +");"
        print(js_string)
        self.page().runJavaScript(js_string)

    def eraseNote(self, key):
        js_string = r'erase_note('+str(key)+');'
        self.page().runJavaScript(js_string)


    def reset(self):
        js_string = r"location.reload();"
        self.page().runJavaScript(js_string)

if __name__ == "__main__":
  app = QApplication([])
  
  '''
  view = ShortWebView()
  btn1 = QPushButton(view)
  def wrapper1():
    view.drawNote(76,"C4", "bass")
  btn1.clicked.connect(wrapper1)

  btn2 = QPushButton(view)
  btn2.setGeometry(QRect(50, 50,50,50))
  def wrapper2():
    view.eraseNote(76)
  btn2.clicked.connect(wrapper2)

  btn3 = QPushButton(view)
  btn3.setGeometry(QRect(100, 50,50,50))
  btn3.clicked.connect(view.reset)
  '''
  view = ShortWebW()

  view.show()

  w = ShortWebView()
  w.show()
  w.resize(300,400)
  print(w.sizeHint())
  print(w.settings())
  #time.sleep(5)
  #view.drawNote(75, "C4")
  #view.eraseNote(75)
  app.exec_()