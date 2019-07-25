import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets, Qt

from display import generate_display
import printwindow as print_w

#ㅡㅡㅡㅡㅡㅡㅡㅡㅡ
#| btn_1 | btn_2 |
#ㅡㅡㅡㅡㅡㅡㅡㅡㅡ
#| btn_3 | btn_4 |
#ㅡㅡㅡㅡㅡㅡㅡㅡㅡ

#test
gui_textlist = [
        ["프로그램 재시작 필요", "-", "-", "-", "-"],
        ["메인 화면", "음성인식 프린트\n시작", "녹음된 음성파일을 이용하여\n프린트", "문서 파일을 이용하여\n프린트", "뉴스기사\n출력하기"],
        ["프린트", "새로 기록", "음성 재안내", "기존파일에 이어서 기록", "뒤로가기"],
        ["녹음파일로 기록", "새로 기록", "음성 재안내", "기존파일에 이어서 기록", "뒤로가기"],
        ["문서파일의 내용을 기록", "문서 선택", "음성 재안내", "기존파일에 이어서 기록", "뒤로가기"],
        ["--기타기능--", "--기타기능--", "--기타기능--", "--기타기능--", "뒤로가기"],
        ["음성프린트", "입력 시작", "음성 재안내", "정정 및 수정", "입력 종료"],
        ["입력중", "이 내용으로 기록", "음성 재안내", "재입력", "입력 종료"],
        ["입력중", "이 내용으로 기록", "음성 재안내", "재입력", "입력 종료"],
        ["입력중", "이 음성 파일로 기록 시작", "음성 재안내", "", "입력 종료"],
        ["파일선택", "위", "파일선택", "아래", "뒤로가기"]
]

class Ui_Dialog(generate_display):
    def __init__(self, mode, fontsize):
        return super().__init__(mode, fontsize)
    
    def set_buttonsize(self) :
        for i in range(4):
            self.mainBtnlist[i].setMinimumSize(QtCore.QSize(300, 175))

    def set_layout(self):
        self.mainLayout_2.setContentsMargins(250, 30, 250, 30)
        self.mainLayout_4.addLayout(self.mainLayout, 1, 0, 1, 1)

    # def set_mode(self, mode):
    #     self.mode = mode

    def hied_dialog(self):
        self.mainDialog.hide()
        mode_list = {
            'print_main' : 'print_dialog',
            'record_main' : 'print_dialog',
            'doc_main' : 'file_dialog',
            'news_main' : 'file_dialog',
            'error' : self.refresh_ui(0)
        }
        return mode_list.get(self.mode, mode_list['error'])
    
    def show_dialog(self):
        self.mainDialog.show()

    def btn_1(self) :
        print('버튼1')
        mode_list = {
            'main' : self.refresh_ui(gui_textlist[2]),
            'print_main' : self.hied_dialog,
            'record_main' : self.hied_dialog,
            'doc_main' : self.hied_dialog,
            'news_main' : self.hied_dialog,
            'error' : self.refresh_ui
        }
        return mode_list.get(self.mode, mode_list['error'])

    def btn_2(self) :
        pass

    def btn_3(self) :
        pass

    def btn_4(self) :
        pass

def main():
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_Dialog('main', 30)
    ui.set_buttonsize()
    ui.set_layout()
    ui.refresh_ui(gui_textlist[1])
    ui.set_clickevent(ui.btn_1, ui.btn_2, ui.btn_3, ui.btn_4)
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()