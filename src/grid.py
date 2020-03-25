import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QPushButton

from longwebw import LongWebW
from shortwebw import ShortWebW
from kbw import KBW


class MainW(QWidget):
    def __init__(self):
      super(MainW, self).__init__()
      self.grid = QGridLayout(self)
      def placeHolder(label, color):
         ql = QLabel(label)
         ql.setStyleSheet('background-color:' + color)
         return ql
      self.longwebw = LongWebW()
      self.shortwebw = ShortWebW()
      self.kbw = KBW()
      # self.grid.addWidget(placeHolder("1", "yellow"), 0, 0, 1, 4)
      self.grid.addWidget(self.longwebw, 0, 0, 1, 4)
      # self.grid.addWidget(placeHolder("2", "blue"), 0, 4, 1, 1)
      self.grid.addWidget(self.shortwebw, 0, 4, 1, 1)
      self.grid.addWidget(placeHolder("3", "green"), 0, 5, 1, 1)
      # self.grid.addWidget(placeHolder("4", "red"), 1, 0, 1, 6)
      self.grid.addWidget(self.kbw, 1, 0, 1, 6)
      # self.longwebw.resize(1000, 900)
      self.resize(1500, 1000)
     
   
if __name__ == '__main__':
   app = QApplication(sys.argv)
   # win = MainWindow();
   win = MainW();
   win.show();
   sys.exit(app.exec_())