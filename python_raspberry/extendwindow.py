import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets, Qt

from python_raspberry.display import generate_display

gui_textlist = {
        'error':["프로그램 재시작 필요", "-", "-", "-", "-"],
        'extend':["파일선택", "위", '파일선택', "아래", "취소"]
}

class Ui_Dialog(generate_display):
    def __init__(self, mode, fontsize, title=None):
        super().__init__(mode, fontsize)
        self.set_buttonsize()
        self.create_listview()
        self.set_layout()
        self.refresh_ui(gui_textlist['extend'])
        self.dex = 0
        self.set_listfocus(self.dex)
        self.set_mode('extend')

        @self.make_voice_btn_extend
        def btn_1_func(self) :
            if self.debug : print('<', __name__, '>', 'btn_1')
            if self.get_mode() == 'extend':
                if self.dex > 0:
                    self.dex -= 1
                    self.set_listfocus(self.dex)

        @self.make_voice_btn_extend  
        def btn_2_func(self) :
            if self.debug : print('<', __name__, '>', 'btn_2')
            self.mode = 'print'
            self.mainDialog.close()

        @self.make_voice_btn_extend
        def btn_3_func(self) :
            if self.debug : print('<', __name__, '>', 'btn_3')
            if self.get_mode() == 'extend':
                if self.dex < (len(self.itemList) - 1):
                    self.dex += 1
                    self.set_listfocus(self.dex)

        self.btn_1 = btn_1_func
        self.btn_2 = btn_2_func
        self.btn_3 = btn_3_func

        self.set_clickevent(self.btn_1, self.btn_2, self.btn_3, self.btn_4)

    def create_listview(self):
        self.itemList = os.listdir('C://')
        self.listView = QtWidgets.QListView()
        self.model = QtGui.QStandardItemModel()
        for item in self.itemList:
            self.model.appendRow(QtGui.QStandardItem(item))
        self.listView.setModel(self.model)
        self.listView.setStyleSheet('font-size:'+str(self.fontsize)+'px;')

    def set_buttonsize(self) :
        for i in range(4):
            self.mainBtn[i].setMinimumSize(QtCore.QSize(300, 75))
    
    def set_layout(self):
        self.mainLayout_2.setContentsMargins(20, 30, 20, 30)
        self.mainLayout_4.addLayout(self.mainLayout_3, 1, 0, 1, 1)
        self.mainLayout_4.addLayout(self.mainLayout, 2, 0, 1, 1)
        self.mainLayout_3.addWidget(self.listView, 0, 0, 1, 1)

    def set_listfocus(self, index):
        self.listView.setFocus()
        self.listView.setCurrentIndex(self.listView.model().index(index,0))
        self.sel_item = self.itemList[index]
        print(self.itemList[index])


    def btn_4(self) :
        if self.debug : print('<', __name__, '>', 'btn_4')
        if self.get_mode() != 'main':
            self.mode = 'main'
            self.mainDialog.close()
    
    def make_voice_btn_extend(self, func):
        self.current_func = None
        def voice():
            if func.__name__ == 'btn_2_func':
                if self.current_func == func.__name__:
                    self.call_voice = self.sel_item
                    self.make_voice()
                    func(self)
                else:
                    self.call_voice = '선택된 아이템 {}를 통해 프린트를 진행합니다. 한번 더 입력하면 결정합니다. 파일포맷이 맞지 않는 파일을 입력하는 경우 프린트를 진행 할 수 없으니 주의해주십시오'.format(self.sel_item)
                    self.make_voice()
                    self.current_func = func.__name__
            else:
                func(self)
                self.call_voice = self.sel_item
                self.make_voice()
        return voice


def main():
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_Dialog('extend', 30)
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()