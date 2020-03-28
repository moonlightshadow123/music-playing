import sys, pickle
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QSizePolicy, QGridLayout, QPushButton
import PyQt5.QtGui

from config import btnNum_btnIdx, btnIdx_noteIdx, noteIdx_noteStr

class Btn(QPushButton):
   def __init__(self, btnIdx, parent, *args,**kwargs):
      super(Btn, self).__init__(*args, **kwargs)
      self.btnIdx = btnIdx
      self.parent = parent
      self.press_color = "#BFBABA"
      self.release_color = "#DBD6D6"
      self.setStyleSheet('background-color:' + self.release_color)
      self.pressed.connect(self.on_press)
      self.released.connect(self.on_release)
   
   def on_press(self):
      self.setStyleSheet('background-color:' + self.press_color)
      if self.parent: self.parent.parent.btnOn(self.btnIdx)

   def on_release(self):
      self.setStyleSheet('background-color:' + self.release_color)
      if self.parent: self.parent.parent.btnOff(self.btnIdx)

class KBW(QWidget):
   def __init__(self, parent):
      super(KBW, self).__init__()
      self.parent = parent
      self.grid = QGridLayout(self)
      self.btn_list = []
      self.cur_btnIdx = 0
      self.genBtns()
      self.key_list = []

   def addBtn(self, row, col, width, height):
      btn = Btn(self.cur_btnIdx, self)
      btn.setSizePolicy(QSizePolicy.MinimumExpanding,QSizePolicy.Preferred)
      self.btn_list.append(btn)
      self.grid.addWidget(btn, row, col, width, height)      
      self.cur_btnIdx += 1

   def genBtns(self):
      self.gen0()
      self.gen1()
      self.gen2()
      self.gen3()
      self.gen4()
      self.gen5()

   def gen0(self):
      for i in range(19):
         self.addBtn(0, i*2, 2, 2)

   def gen1(self):
      for i in range(13):
         self.addBtn(2, i*2, 2, 2)
      self.addBtn(2, 13*2, 2, 4)
      for i in range(4):
         self.addBtn(2, 13*2+4+i*2, 2, 2)

   def gen2(self):
      self.addBtn(4, 0, 2, 3)
      for i in range(12):
         self.addBtn(4, 3+i*2, 2, 2)
      self.addBtn(4, 3+12*2, 2, 3)
      for i in range(3):
         self.addBtn(4, 3+12*2+3+i*2, 2, 2)
      self.addBtn(4, 3+12*2+3+3*2, 4, 2)

   def gen3(self):
      self.addBtn(6, 0, 2, 4)
      for i in range(11):
         self.addBtn(6, 4+i*2, 2, 2)
      self.addBtn(6, 4+11*2, 2, 4)
      for i in range(3):
         self.addBtn(6, 4+11*2+4+i*2, 2, 2)

   def gen4(self):
      self.addBtn(8, 0, 2, 5)
      for i in range(10):
         self.addBtn(8, 5+i*2, 2, 2)
      self.addBtn(8, 5+10*2, 2, 3)
      for i in range(4):
         self.addBtn(8, 5+10*2+3+i*2, 2, 2)
      self.addBtn(8, 5+10*2+3+4*2, 4, 2)

   def gen5(self):
      for i in range(3):
         self.addBtn(10, i*3, 2, 3)
      self.addBtn(10, 3*3, 2, 11)
      for i in range(8):
         self.addBtn(10, 3*3+11+i*2, 2, 2)

   def keyPressEvent(self, event):
      if not event.isAutoRepeat():
         print(str(len(self.key_list)) + ": " + str(event.key()) + ": "+ event.text())
         # self.key_list.append(event.key())
         btnIdx = btnNum_btnIdx[event.key()]
         self.btn_list[btnIdx].pressed.emit()

   def keyReleaseEvent(self, event):
      if not event.isAutoRepeat():
         print(str(len(self.key_list)) + ": " + str(event.key()))
         # self.key_list.append(event.key())
         btnIdx = btnNum_btnIdx[event.key()]
         self.btn_list[btnIdx].released.emit()

   def dump(self):
      with open("key_list.pkl", "wb") as f:
         pickle.dump(self.key_list, f)

   def load(self):
      with open("key_list.pkl", "rb") as f:
         self.key_list = pickle.dump(f)


if __name__ == '__main__':
   app = QApplication(sys.argv)
   # win = MainWindow();
   win = KBW(None)
   win.show()
   app.exec_()
   # win.dump()