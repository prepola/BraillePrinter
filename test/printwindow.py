import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets, Qt

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from display import generate_display
from python_raspberry import stt
import tts

gui_textlist = {
        'error':["프로그램 재시작 필요", "-", "-", "-", "-"],
        'print':["음성프린트", "입력 시작", "음성 재안내", "정정 및 수정", "입력 종료"],
        'print_title':["입력 중", "이 내용으로 기록", "음성 재안내", "재입력", "입력 종료"],
        'print_body':["입력 중", "이 내용으로 기록", "음성 재안내", "재입력", "입력 종료"],
        'print_input':["입력 중", "입력 중", "입력 중", "입력 중", "입력 중"]
}

work_textdic = {
        'duplicate':'중복되는 파일이 존재합니다.\n다시 시도해주십시요.',
        'start':'안녕하세요\n입력시작 버튼을 누르면 입력을 시작합니다.',
        'readytitle':'기록을 시작하기전에 제목을 입력해야 합니다.\n준비가 되었다면 좌측 상단 버튼을 눌러 제목을 입력해주세요.',
        'readybody':'본문 입력을 시작합니다.\n좌측 상단 버튼을 눌러 기록을 시작해 주십시오',
        'readyrecord':'해당파일로 입력을 시작합니다.',
        'fatal':'비정상 종료됨\n입력종료 버튼을 눌러주세요.',
        'overtime':'입력 시간이 초과하였거나 입력에 실패하였습니다.\n다시 시도해주십시요.',
        'isright':'다음 내용이 맞습니까?',
        'commit':'입력되었습니다\n다음줄로 이동합니다.'
}

credential_path = 'C:\\Users\\jk691\\Documents\\hanium project-3d7b2a095e96.json'

class Ui_Dialog(generate_display):
    def __init__(self, mode, fontsize):
        super().__init__(mode, fontsize)

        self.play_voice = None

        self.create_worktable()
        self.set_buttonsize()
        self.set_layout()
        self.refresh_ui(gui_textlist[self.get_mode('start')])

    def create_worktable(self):
        self.workTable = QtWidgets.QTextBrowser(self.mainDialog)
        self.workTable.setMinimumSize(QtCore.QSize(0, 245))
        self.workTable.setMaximumSize(QtCore.QSize(1200, 245))
        self.workTable.setStyleSheet('font-size:'+str(self.fontsize)+'px;')

    def set_buttonsize(self) :
        for i in range(4):
            self.mainBtn[i].setMinimumSize(QtCore.QSize(300, 75))
    
    def set_layout(self):
        self.mainLayout_2.setContentsMargins(20, 30, 20, 30)
        self.mainLayout_4.addLayout(self.mainLayout_3, 1, 0, 1, 1)
        self.mainLayout_4.addLayout(self.mainLayout, 2, 0, 1, 1)
        self.mainLayout_3.addWidget(self.workTable, 0, 0, 1, 1)

    def get_mode(self, text=None):
        if text is not None:
            if self.play_voice is not None:
                self.play_voice.stop()
                self.play_voice = None
            self.workTable.append(work_textdic[text])
            tts.make_voice(work_textdic[text])
            self.play_voice = tts.run_voice()
            self.play_voice.start()
        return super().get_mode()

# TODO: 수정해야 되는 부분

    def print_title(self):
        print("음성프린트 기능을 클릭 하셨습니다.")
        while 1:
            self.dis[1].set_infotext(work_textdic['readytitle'])
            if isinstance(self.select_item,str):
                self.dis[1].set_infotext('파일 '+self.select_item+' 로 시작합니다.')
                return self.select_item
            try:
                title_word = stt.trans(credential_path)
            except:
                print("bad auth JSON")
                self.dis[1].set_infotext(work_textdic['fatal'])
                break
            if not isinstance(title_word,str) | (len(title_word) < 1):
                self.dis[1].set_infotext(work_textdic['overtime'])
                continue
            self.dis[1].set_infotext(title_word)
            self.dis[1].set_infotext(work_textdic['isright'])

            # if os.path.isfile('/mnt/usb'+title_word+'.txt'): # 라즈베리파이
            if os.path.isfile(title_word+'.txt'):
                self.dis[1].set_infotext(work_textdic['duplicate'])
                title_word = None
                continue
            else:
                self.dis[1].set_infotext('파일 '+title_word+' 로 시작합니다.')
                return title_word

    def print_body(self):
            self.dis[1].set_infotext(work_textdic['readybody'])
            while 1:
                try:
                    typing_text = stt.trans(credential_path)
                except:
                    print("bad auth JSON")
                    self.dis[1].set_infotext(work_textdic['fatal'])
                    break

                if not isinstance(typing_text,str):
                    self.dis[1].set_infotext(work_textdic['overtime'])
                    continue
                self.dis[1].set_infotext(typing_text)
                self.dis[1].set_infotext(work_textdic['isright'])
                return typing_text

    def print_record(self, record_name):
        # print("녹음프린트 기능을 클릭 하셨습니다.")
        record_text = stt.record(record_name, credential_path)
        return record_text

    def commit_text(self, title_word, input_text):
        # with open('/mnt/usb'+title_word+'.txt','w') as fileh: # 라즈베리파이
        if title_word[-4:] != '.txt':
            title_word = title_word+'.txt'
        with open(title_word,'a') as fileh:
            fileh.write(input_text+'\n')  

# TODO: 여기까지

    def btn_1(self) :
        if self.get_mode('readytitle') == 'print':
            self.set_mode('print_title')
            self.refresh_ui(gui_textlist[self.get_mode()])
        elif self.get_mode() == 'print_title':
            self.set_mode('print_input')
            self.refresh_ui(gui_textlist[self.get_mode()])

    def btn_2(self) :
        if self.get_mode() == 'print':
            self.set_mode('record_main')
            self.refresh_ui(gui_textlist[self.get_mode()])

    def btn_3(self) :
        if self.get_mode() == 'print':
            self.set_mode('doc_main')
            self.refresh_ui(gui_textlist[self.get_mode()])

    def btn_4(self) :
        if self.get_mode() != 'print':
            self.set_mode('main')
            print('main으로 재전환')
    
def main():
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_Dialog('print',30)
    ui.mainDialog.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()