import sys
import os
from PyQt5 import QtWidgets

from printwindow import Ui_Dialog as w_rin
from mainwindow import Ui_Dialog as w_main
from extendwindow import Ui_Dialog as w_ext

gui_textlist = [
        ["프로그램 재시작 필요", "-", "-", "-", "-"],
        ["메인 화면", "음성인식 프린트\n시작", "녹음된 음성파일을 이용하여\n프린트", "문서 파일을 이용하여\n프린트", "뉴스기사\n출력하기"],
        ["프린트", "새로 기록", "음성 재안내", "기존파일에 이어서 기록", "뒤로가기"],
        ["녹음파일로 기록", "새로 기록", "음성 재안내", "기존파일에 이어서 기록", "뒤로가기"],
        ["문서파일의 내용을 기록", "문서 선택", "음성 재안내", "기존파일에 이어서 기록", "뒤로가기"],
        ["--기타기능--", "--기타기능--", "--기타기능--", "--기타기능--", "뒤로가기"],
        ["음성프린트", "입력 시작", "음성 재안내", "정정 및 수정", "입력 종료"],
        ["입력중", "이 내용으로 기록", "음성 재안내", "재입력", "입력 종료"],
        ["입력중", "이 음성 파일로 기록 시작", "음성 재안내", "", "입력 종료"],
        ["파일선택", "위", "파일선택", "아래", "뒤로가기"]
]

class mode(object):
    def __init__(self, mode, dis):        
        self.mode = ''
        app = QtWidgets.QApplication(sys.argv)
        self.window = dis(30)
        sys.exit(app.exec_())

        self.main_mode_list = {
            'main' : self.window.set_mode('main'),
            'print_main' : self.window.refresh_ui(gui_textlist[2]),
            'record_main' : self.window.refresh_ui(gui_textlist[3]),
            'doc_main' : self.window.refresh_ui(gui_textlist[4]),
            'news_main' : self.window.refresh_ui(gui_textlist[5]),
            'error' : self.window.refresh_ui(gui_textlist[0])
        }
        self.print_mode_list = {
            'print_first' : self.window.refresh_ui(gui_textlist[5]),
            'print_ready' : self.window.refresh_ui(gui_textlist[5]),
            'is_right' : self.window.refresh_ui(gui_textlist[5]),
            'next_line' : self.window.refresh_ui(gui_textlist[5]),
            'print_end' : self.window.refresh_ui(gui_textlist[5]),
            'error' : self.window.refresh_ui(gui_textlist[0])
        }

        self.extend_mode_list = {
            'sel_flie' : self.window.refresh_ui(gui_textlist[5]),
            'is_right' : self.window.refresh_ui(gui_textlist[5]),
            'error' : self.window.refresh_ui(gui_textlist[0])
        }

        print('선언완료')
        self.set_mode(mode)
        self.set_display(dis)

    def set_mode(self, mode):
        print('----------',mode, self.mode)
        if self.mode != mode:
            for mode_list in [self.main_mode_list, self.print_mode_list, self.extend_mode_list]:
                if mode in mode_list:
                    return mode_list.get(mode, mode_list['error'])

        self.mode = mode

    def set_display(self, dis):
        self.window = dis

def main():
    ui = mode('main', w_main)


if __name__ == "__main__":
    main()