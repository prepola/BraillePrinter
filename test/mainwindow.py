import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets, Qt

from display import generate_display
from printwindow import Ui_Dialog as printDialog
from extendwindow import Ui_Dialog as extendDialog

#ㅡㅡㅡㅡㅡㅡㅡㅡㅡ
#| btn_1 | btn_2 |
#ㅡㅡㅡㅡㅡㅡㅡㅡㅡ
#| btn_3 | btn_4 |
#ㅡㅡㅡㅡㅡㅡㅡㅡㅡ

#test
gui_textlist = {
        'error':["프로그램 재시작 필요", "-", "-", "-", "-"],
        'main':["메인 화면", "음성인식 프린트\n시작", '음성 재안내', "녹음된 음성파일을 이용하여\n프린트", "문서 파일을 이용하여\n프린트"],
        'print_main':["프린트", "새로 기록", "음성 재안내", "기존파일에 이어서 기록", "뒤로가기"],
        'record_main':["녹음파일로 기록", "새로 기록", "음성 재안내", "기존파일에 이어서 기록", "뒤로가기"],
        'doc_main':["문서파일의 내용을 기록", "문서 선택", "음성 재안내", "기존파일에 이어서 기록", "뒤로가기"]
}

class Ui_Dialog(generate_display):
    def __init__(self, mode, fontsize):
        super().__init__(mode, fontsize)
        self.set_buttonsize()
        self.set_layout()
        self.refresh_ui(gui_textlist['main'])
        self.set_clickevent(self.btn_1, self.btn_2, self.btn_3, self.btn_4)

    def set_buttonsize(self) :
        for i in range(4) :
            self.mainBtn[i].setMinimumSize(QtCore.QSize(300, 175))
            
    def set_layout(self):
        self.mainLayout_2.setContentsMargins(250, 30, 250, 30)
        self.mainLayout_4.addLayout(self.mainLayout, 1, 0, 1, 1)
    
    def show_dialog(self):
        return self.mainDialog.show()

    def btn_1(self) :
        if self.get_mode() == 'main':
            self.set_mode('print_main')
            self.refresh_ui(gui_textlist[self.get_mode()])
        elif self.get_mode() == 'print_main':
            self.set_mode('print')
            self.mainDialog.close()

    def btn_2(self) :
        pass

    def btn_3(self) :
        if self.get_mode() == 'main':
            self.set_mode('record_main')
            self.refresh_ui(gui_textlist[self.get_mode()])

    def btn_4(self) :
        if self.get_mode() == 'main':
            self.set_mode('doc_main')
            self.refresh_ui(gui_textlist[self.get_mode()])
        elif self.get_mode() != 'main':
            self.set_mode('main')
            self.refresh_ui(gui_textlist[self.get_mode()])

def main():
    app = QtWidgets.QApplication(sys.argv)
    mui = Ui_Dialog('main', 30)
    mui.show_dialog()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()