# -*- coding: utf-8 -*-

import sys
import io
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
# from python_raspberry import stt
from PyQt5 import QtWidgets, Qt
import display as dis

# 1: print_ui
# 2: recording_file_ui
# 3: document_ui
# 4: undefined_ui
# 5: title_input
# 6: body_input
# 7: feedback_ui
# 8: extend_file
# others: main_ui
mod_list = [1, 2, 3, 4, 5, 6, 7, 8]
fontsize_1 = 30

gui_textlist = [
        ["메인 화면", "음성인식 프린트\n시작", "녹음된 음성파일을 이용하여\n프린트", "문서 파일을 이용하여\n프린트", "--기타기능--"],
        ["프린트", "새로 기록", "음성 재안내", "기존파일에 이어서 기록", "뒤로가기"],
        ["녹음파일로 기록", "새로 기록", "음성 재안내", "기존파일에 이어서 기록", "뒤로가기"],
        ["문서파일의 내용을 기록", "문서 선택", "음성 재안내", "기존파일에 이어서 기록", "뒤로가기"],
        ["--기타기능--", "--기타기능--", "--기타기능--", "--기타기능--", "뒤로가기"],
        ["음성프린트", "입력 시작", "음성 재안내", "정정 및 수정", "입력 종료"],
        ["입력중", "이 내용으로 기록", "음성 재안내", "재입력", "입력 종료"],
        ["입력중", "이 내용으로 기록", "음성 재안내", "재입력", "입력 종료"],
        ["파일선택", "위", "파일선택", "아래", "뒤로가기"]
]
work_textdic = {
        'duplicate':'중복되는 파일이 존재합니다.\n다시 시도해주십시요.',
        'start':'안녕하세요\n기록을 시작하기전에 제목을 입력해야 합니다.\n',
        'readytitle':'준비가 되었다면 좌측 상단 버튼을 눌러 제목을 입력해주세요.',
        'readybody':'좌측 상단 버튼을 눌러 기록을 시작합니다.',
        'fatal':'비정상 종료됨\n입력종료 버튼을 눌러주세요.',
        'overtime':'입력 시간이 초과하였거나 입력에 실패하였습니다.\n다시 시도해주십시요.',
        'isright':'다음 내용이 맞습니까?',
        'newline':'다음줄로 이동합니다.'
}

class Ui_Dialog(object):
    mod_num = int()
    dex = 0
    title = None
    typing_text = None

    def __init__(self):
        self.Dis = [
                dis.Ui_Dialog("main",fontsize_1), 
                dis.Ui_Dialog("print",fontsize_1),
                dis.Ui_Dialog("extend",fontsize_1)
        ]

        for i in range(3):
            self.Dis[i].mainBtnlist[0].clicked.connect(self.btn_1)
            self.Dis[i].mainBtnlist[1].clicked.connect(self.btn_2)
            self.Dis[i].mainBtnlist[2].clicked.connect(self.btn_3)
            self.Dis[i].mainBtnlist[3].clicked.connect(self.btn_back)

        self.change_dialog(self.mod_num, None)
        self.refresh_ui(self.mod_num)

    def refresh_ui(self, mod_num):
        for i in range(5):
            if mod_num not in mod_list: mod_num = 0
            elif mod_num >= 8 :
                if i == 0 : self.Dis[2].mainInfo.setText(gui_textlist[mod_num][i])
                else: self.Dis[2].mainBtnlist[i-1].setText(gui_textlist[mod_num][i])
            elif mod_num >= 5 :
                if i == 0 : self.Dis[1].mainInfo.setText(gui_textlist[mod_num][i])
                else: self.Dis[1].mainBtnlist[i-1].setText(gui_textlist[mod_num][i])
            if i == 0 : self.Dis[0].mainInfo.setText(gui_textlist[mod_num][i])          
            else : self.Dis[0].mainBtnlist[i-1].setText(gui_textlist[mod_num][i])
        print(self.mod_num,gui_textlist[mod_num][0])
    
    def btn_1(self):
        if self.mod_num not in mod_list:
            self.mod_num = 1
            self.refresh_ui(self.mod_num)
        elif (self.mod_num == 1):
            self.mod_num = 5
            self.change_dialog(self.mod_num, 'print')
        elif (self.mod_num == 2):
            self.print_record()
        elif (self.mod_num == 3):
            self.print_document()
        elif (self.mod_num == 4):
            self.others()
        elif (self.mod_num == 5):
            self.mod_num = 6
            self.change_dialog(self.mod_num, 'print')
            self.title = self.print_title()
        elif (self.mod_num == 6):
            self.mod_num = 7
            self.body = self.print_body()
        elif (self.mod_num == 7):
            self.mod_num = 6
            self.commit_text(self.title, self.body)
        elif (self.mod_num == 8):
            if self.dex > 0:
                self.dex = self.dex - 1
                self.set_listfocus(self.dex)
        
    def btn_2(self):
        if self.mod_num not in mod_list:
            self.mod_num = 3
            self.refresh_ui(self.mod_num)
            self.print_document()
        elif (self.mod_num == 1):
            self.noone()
        elif (self.mod_num == 2):
            self.noone()
        elif (self.mod_num == 3):
            self.noone()
        elif (self.mod_num == 4):
            self.others()

    def btn_3(self):
        if self.mod_num not in mod_list:
            self.mod_num = 2
            self.refresh_ui(self.mod_num)
            self.print_record()
        elif (self.mod_num in [1, 2, 3]):
            self.mod_num = 8
            self.change_dialog(self.mod_num, 'extend')
            self.set_listfocus(self.dex)
        elif (self.mod_num == 4):
            self.others()
        elif (self.mod_num == 8):
            if self.dex < (len(self.Dis[2].itemList) - 1):
                self.dex = 1 + self.dex
                self.set_listfocus(self.dex)

    def btn_back(self):
        if self.mod_num in mod_list:
            self.Dis[1].workTable.setText('')
            self.dex = 0
            self.title = None
            self.typing_text = None
            self.mod_num = 0
            self.refresh_ui(self.mod_num)
            if self.Dis[1].mainDialog.isVisible() | self.Dis[2].mainDialog.isVisible():
                self.change_dialog(self.mod_num, None)              
            print("뒤로")
    
    def change_dialog(self, mod_num, to_dialog):
        self.refresh_ui(mod_num)
        if to_dialog == 'print':
            self.Dis[0].mainDialog.hide()
            self.Dis[1].mainDialog.show()
        elif to_dialog == 'extend':
            self.Dis[0].mainDialog.hide()
            self.Dis[2].mainDialog.show()
            self.extend_file()
        else:
            self.Dis[0].mainDialog.show()
            self.Dis[1].mainDialog.hide()
            self.Dis[2].mainDialog.hide()  

    def set_listfocus(self, index):
        self.Dis[2].listView.setFocus()
        self.Dis[2].listView.setCurrentIndex(self.Dis[2].listView.model().index(index,0))
        select_item = self.Dis[2].itemList[index]
        print(select_item)
    
    def print_title(self):
        # print("음성프린트 기능을 클릭 하셨습니다.")
        self.Dis[1].workTable.setText(work_textdic['start'])
        while 1:
            self.Dis[1].workTable.append(work_textdic['readytitle'])
            try:
                title_word = stt.trans()
            except:
                print("bad auth JSON")
                self.Dis[1].workTable.append(work_textdic['fatal'])
                break

            if not isinstance(title_word,str):
                self.Dis[1].workTable.append(work_textdic['overtime'])
                continue
            self.Dis[1].workTable.append(title_word)
            self.Dis[1].workTable.append(work_textdic['isright'])

            # if os.path.isfile('/mnt/usb'+title_word+'.txt'): # 라즈베리파이
            if os.path.isfile(title_word+'.txt'):
                self.Dis[1].workTable.append(work_textdic['duplicate'])
                title_word = None
                continue
            else:
                return title_word

    def print_body(self):
            self.Dis[1].workTable.append(work_textdic['readybody'])
            while 1:
                typing_text = stt.trans()

                if not isinstance(typing_text,str):
                    self.Dis[1].workTable.append(work_textdic['overtime'])
                    continue
                self.Dis[1].workTable.append(typing_text)
                self.Dis[1].workTable.append(work_textdic['isright'])
                return typing_text

    def commit_text(self, title_word, typing_text):
        # with open('/mnt/usb'+title_word+'.txt','w') as fileh: # 라즈베리파이
        with open(title_word+'.txt','a') as fileh:
            fileh.write(typing_text+'\n')  
        self.Dis[1].workTable.append(work_textdic['newline'])

    def print_record(self):
        print("녹음프린트 기능을 클릭 하셨습니다.")

    def print_document(self):
        print("문서프린트 기능을 클릭 하셨습니다.")
    
    def others(self):
        print("기타 기능을 클릭 하셨습니다.")
    
    def extend_file(self):
        print("외부파일 기능을 클릭 하셨습니다.")

    def noone(self):
        return None

def main():
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_Dialog()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()