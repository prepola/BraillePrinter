# -*- coding: utf-8 -*-
import zipfile, re
import xml.etree.ElementTree as ET

def str_init (str_temp, str_text, bool_row, int_word) :
    if (bool_row == False) & (str_temp != None) :
        return str_temp
    elif (bool_row == True) & (str_temp != None) :
        if (str_temp != '') & (int_word < 2) :
            str_temp = str_temp + ' | ' # ?��?�� �? ?��?�� 구분
    if str_temp == None : return str_text
    str_temp = str_temp + str_text
    return str_temp

def out_process (data) :
    print(data)
    return None

temp = str()
matrix_state = False
row_state = False 
word_num = 0 # 공백?�� ?��?�� Text Element?��?�� 공백문자�? ?��?��?��?�� 것을 방�???���? ?��?�� �??��
file_name = str()
ns = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'

while True :
    try :
        file_name = input('?��?��명을 ?��?��?��?�� 주십?��?�� :')
        if len(file_name) < 1 : file_name = 'test.docx' # ?��버그
        elif file_name[-5:] != '.docx' : file_name = file_name + '.docx'
        docx = zipfile.ZipFile(file_name)
        context = docx.read('word/document.xml')
    except :
        out_process('?��못된 ?��?�� ?��?��')
        break
    
    tree = context.decode()
    root = ET.fromstring(tree)
    tree_list = root.iter()

    print(tree)

    for node in tree_list:
        if node.tag == ns + 'tr' : # ?�� 구분 ?���?
            matrix_state = True
            if temp != '' : # ?�� 마무리시 temp?�� ????��?�� text 출력
                out_process(str_init(temp, node.text, False, word_num))
                temp = 'tr?�� ?��?��?�� 초기?�� ?��'
        elif node.tag == ns + 'tc' : # ?�� 구분 ?���?
            if row_state == False : row_state = True
            elif word_num != 0 : word_num = 0
        elif node.tag == ns + 'p' :
            if word_num != 0 : word_num = 0
        elif node.tag == ns + 't' : # Text Element
            word_num = word_num + 1      
            if matrix_state == False : out_process(str_init(None, node.text, False, word_num))
            elif matrix_state == True : temp = str_init(temp, node.text, row_state, word_num)
        elif node.tag == ns + 'spacing' :
            temp = temp + '\t'
        elif node.tag == ns + 'bookmarkStart' : # ?��?�� ?��?�� ?���?
            out_process('-'*10 + '?��?��?��?��' + '-'*10)
        elif node.tag == ns + 'bookmarkEnd': # ?��?�� 종료 ?���?
            matrix_state = False
            row_state = False
            out_process(str_init(temp, node.text, False, word_num))
            temp = '북마?��?��?���? ?��?��?�� 초기?��?��'
            out_process('-'*10 + '?��?��종료' + '-'*10)
        print(node.tag) # ?��버그