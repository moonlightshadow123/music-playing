import sys, os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QPushButton, QSizePolicy
from PyQt5.QtWebEngineWidgets import QWebEngineView      

from PyQt5.QtCore import QObject,  QUrl,  QRect

class LongWebW(QWidget):
    def __init__(self):
      super(LongWebW, self).__init__()
      self.grid = QGridLayout(self)
      self.view_list = [LongWebView(), LongWebView()]
      self.view_list[0].setSizePolicy(QSizePolicy.MinimumExpanding,QSizePolicy.Preferred)
      self.view_list[1].setSizePolicy(QSizePolicy.MinimumExpanding,QSizePolicy.Preferred)
      self.grid.addWidget(self.view_list[0], 0,0,1,1)
      self.grid.addWidget(self.view_list[1], 1,0,1,1)
      self.setMinimumWidth(1200)
      self.setFixedHeight(700)  

class LongWebView(QWebEngineView):
   def __init__(self):
      super(LongWebView, self).__init__()
      self.file_name = "longweb.html"

      file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, "web" , self.file_name))
      local_url = QUrl.fromLocalFile(file_path)
      self.load(local_url)


if __name__ == '__main__':
   app = QApplication(sys.argv)
   # win = MainWindow();
   win = LongWebW();
   win.show();
   sys.exit(app.exec_())