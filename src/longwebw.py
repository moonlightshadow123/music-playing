import sys, os, threading, time, copy
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QPushButton, QSizePolicy
from PyQt5.QtWebEngineWidgets import QWebEngineView      

from PyQt5.QtCore import QObject,  QUrl,  QRect
from songs_parser import Parser
from osc import OSC
from utils import wait_until, merge2list, addToSet, VStrToNIdx

class LongWebW(QWidget):
    def __init__(self):
        super(LongWebW, self).__init__()
        self.grid = QGridLayout(self)
        self.osc = OSC()
        self.osc.clear()
        self.view_list = [LongWebView(), LongWebView()] 
        self.view_list[0].setSizePolicy(QSizePolicy.MinimumExpanding,QSizePolicy.Preferred)
        self.view_list[1].setSizePolicy(QSizePolicy.MinimumExpanding,QSizePolicy.Preferred)
        self.onData_list = [[], []] # [[(cur_set, onset),], [(cur_set, onset),]
        self.offData_list = [[], []] # [[(cur_set, offset),], [(cur_set, offset),]
        self.onOff_list = [[], []]
        self.grid.addWidget(self.view_list[0], 0,0,1,1)
        self.grid.addWidget(self.view_list[1], 1,0,1,1)
        self.setMinimumWidth(1200)
        self.setFixedHeight(700)
        self.cur_notes_set = set()
        self.lock = threading.RLock()
        self.idx = 0
        self.auto = False
        self.renewParserT("molihua.abc")

    def closeEvent(self, event):
        print("longwebw close!!")
        self.auto = False
        self.clear()
        self.osc.clear() 

    def clear(self):
        for note in copy.copy(self.cur_notes_set):
            self.noteOff(note)

    def mousePressEvent(self, event):
        print("clicked")
        if self.auto: 
            self.auto = False
            return
        t = threading.Timer(0.1, self.autoPlay)
        t.start()

    def renewParserT(self, file_name):
        self.view_list[0].refresh()
        self.view_list[1].refresh()
        timer = threading.Timer(2 ,self.renewParser, [file_name])
        timer.start()

    def renewParser(self, file_name):
        self.idx = 0;
        self.parser = Parser(file_name)
        self.view_list[0].set_m_k(self.parser.time_sign, self.parser.key_sign).draw_stave()
        self.view_list[1].set_m_k(self.parser.time_sign, self.parser.key_sign).draw_stave()
        self.give_data(0)
        self.give_data(1)
        self.view_list[0].draw_line()
   
    def noteOn(self, nstr, checkMove=True):
        with self.lock:
            self.cur_notes_set.add(nstr)
            if checkMove: self.check_move()
        NIdx = VStrToNIdx(nstr)
        if NIdx >=0: self.osc.noteOn(NIdx)
        

    def noteOff(self, nstr):
        with self.lock:
            if nstr in self.cur_notes_set:
                self.cur_notes_set.remove(nstr)
        NIdx = VStrToNIdx(nstr)
        if NIdx >=0: self.osc.noteOff(NIdx)

    def check_move(self):
        if self.onData_list[self.idx] != [] and self.onData_list[self.idx][0][0].issubset(self.cur_notes_set): # self.cur_notes_set  == self.onData_list[self.idx][0][0]:
            # have to move
            self.onData_list[self.idx].pop(0)
            self.view_list[self.idx].move()
            if self.onData_list[self.idx] == []:
                # last element, have to fetch
                self.give_data(self.idx)
                self.idx = (self.idx+1)%2
                if self.onData_list[self.idx] != []:
                    self.view_list[self.idx].draw_line()

    def set_move_speed(self, speed):
        self.view_list[0].set_move_speed(speed)
        self.view_list[1].set_move_speed(speed)

    def autoPlay(self):
        if self.onData_list[self.idx] == []: return
        self.auto = True
        cur_onset, cur_onval = self.onData_list[self.idx][0]
        ooIdx = 0
        # Jump to current onoff Idx
        while ooIdx < len(self.onOff_list[self.idx]) and self.onOff_list[self.idx][ooIdx][0] != cur_onval:
            ooIdx += 1
            print("ooIdx = " + str(ooIdx))
        start_time = time.time(); cur_sidx = self.idx
        start_val = cur_onval
        self.clear()
        # Start playing
        while self.auto == True and (ooIdx < len(self.onOff_list[self.idx]) or cur_sidx != self.idx):
            if cur_sidx != self.idx: # Rotate to next idx
                ooIdx = 0; cur_sidx = self.idx
                print("Cur Notes Set:::::::" + str(self.cur_notes_set))
                print(self.onOff_list[self.idx][ooIdx:])
                if len(self.onOff_list[self.idx]) == 0: break # No onoff any more
            val, onset, offset = self.onOff_list[self.idx][ooIdx]
            # Sleep until the val
            self.sleep(start_time, start_val, val, self.parser.speed)
            if ooIdx == 0: self.clear()
            with self.lock:
                for each in offset:
                    self.noteOff(each)
                for each in onset:
                    self.noteOn(each, False)
                self.check_move()
            ooIdx += 1
        self.auto = False

    def sleep(self, start_time, start_val ,val, speed):
        target_time = start_time  + (val - start_val)/speed*60
        while time.time() < target_time:
            time.sleep(0.01) 

    def give_data(self, idx):
        data = self.parser.getNext()
        self.build_data_list(data, idx)
        self.build_view_list(data, idx)

    def build_data_list(self, data, idx):
        tre_data = data['tre_notes_raw']
        bas_data = data['bas_notes_raw']
        self.onData_list[idx] = merge2list(tre_data, bas_data,
                                    lambda cur_data: cur_data[0][3],
                                    addToSet, 
                                    lambda res, key, set1, set2: res.append((set1.union(set2), key)),
                                    set(["|"]))
        print("onData_list!!!!!!!!!!!!!")
        print(self.onData_list)
        self.offData_list[idx] = merge2list(tre_data, bas_data,
                                    lambda cur_data: cur_data[0][4],
                                    addToSet,
                                    lambda res, key, set1, set2: res.append((set1.union(set2), key)),
                                    set(["|"]))
        def res_onoff(cur_set, cur_data):
            for each in cur_data[0]:
                cur_set.add(each)
            print(cur_set)
        def append_onoff(res, key, cur_set1, cur_set2):
            print(key, cur_set1, cur_set2)
            res.append((key, cur_set1, cur_set2))
        self.onOff_list[idx] = merge2list(self.onData_list[idx], self.offData_list[idx],
                                    lambda cur_data: cur_data[1],
                                    res_onoff, # lambda cur_set, cur_data: cur_set.union(cur_data[0]),
                                    append_onoff)
        print("onOff_list!!!!!!!!!!!!!")
        print(self.onOff_list)

    def build_view_list(self, data, idx):
        view = self.view_list[idx]
        view.draw_stave()
        view.draw_notes(data)


class LongWebView(QWebEngineView):
    def __init__(self):
        super(LongWebView, self).__init__()
        self.file_name = "longweb.html"
        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, "web" , self.file_name))
        self.local_url = QUrl.fromLocalFile(file_path)  
        self.load(self.local_url)
        
    def refresh(self):
        js_string = "location.reload();"
        self.page().runJavaScript(js_string)
        return self

    def set_m_k(self, measure, key):
        js_string = 'set_m_k("'+measure+'", "'+key+'");'
        self.page().runJavaScript(js_string)
        return self

    def set_move_speed(self, speed):
        js_string = 'set_move_speed('+str(speed)+');'
        self.page().runJavaScript(js_string)

    def draw_stave(self):
        print("Draw Stave!!")
        js_string = 'draw_stave();'
        self.page().runJavaScript(js_string)

    def draw_notes(self, data):
        js_string = 'draw_notes('+str(data)+');'
        self.page().runJavaScript(js_string)
        print(js_string)

    def draw_line(self):
        js_string = 'draw_line();'
        self.page().runJavaScript(js_string)

    def move(self):
        js_string = 'move();'
        self.page().runJavaScript(js_string)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # win = MainWindow();
    win = LongWebW();
    win.show();
    print("hello")
    sys.exit(app.exec_())