# -*- coding: utf-8 -*-
import zipfile, re
import xml.etree.ElementTree as ET

def str_init (str_temp, str_text, bool_row, int_word) :
    if (bool_row == False) & (str_temp != None) :
        return str_temp
    elif (bool_row == True) & (str_temp != None) :
        if (str_temp != '') & (int_word < 2) :
            str_temp = str_temp + ' | ' # ?–‰?˜ ê°? ?š”?†Œ êµ¬ë¶„
    if str_temp == None : return str_text
    str_temp = str_temp + str_text
    return str_temp

def out_process (data) :
    print(data)
    return None

temp = str()
matrix_state = False
row_state = False 
word_num = 0 # ê³µë°±?´ ?—†?Š” Text Element?—?„œ ê³µë°±ë¬¸ìžê°? ?‚½?ž…?˜?Š” ê²ƒì„ ë°©ì???•˜ê¸? ?œ„?•œ ë³??ˆ˜
file_name = str()
ns = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'

while True :
    try :
        file_name = input('?ŒŒ?¼ëª…ì„ ?ž…? ¥?•˜?—¬ ì£¼ì‹­?‹œ?˜¤ :')
        if len(file_name) < 1 : file_name = 'test.docx' # ?””ë²„ê·¸
        elif file_name[-5:] != '.docx' : file_name = file_name + '.docx'
        docx = zipfile.ZipFile(file_name)
        context = docx.read('word/document.xml')
    except :
        out_process('?ž˜ëª»ëœ ?›Œ?“œ ?ŒŒ?¼')
        break
    
    tree = context.decode()
    root = ET.fromstring(tree)
    tree_list = root.iter()

    print(tree)

    for node in tree_list:
        if node.tag == ns + 'tr' : # ?–‰ êµ¬ë¶„ ?ƒœê·?
            matrix_state = True
            if temp != '' : # ?–‰ ë§ˆë¬´ë¦¬ì‹œ temp?— ????ž¥?œ text ì¶œë ¥
                out_process(str_init(temp, node.text, False, word_num))
                temp = 'tr?— ?˜?•´?„œ ì´ˆê¸°?™” ?¨'
        elif node.tag == ns + 'tc' : # ?—´ êµ¬ë¶„ ?ƒœê·?
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
        elif node.tag == ns + 'bookmarkStart' : # ?–‰? ¬ ?‹œ?ž‘ ?ƒœê·?
            out_process('-'*10 + '?–‰? ¬?‹œ?ž‘' + '-'*10)
        elif node.tag == ns + 'bookmarkEnd': # ?–‰? ¬ ì¢…ë£Œ ?ƒœê·?
            matrix_state = False
            row_state = False
            out_process(str_init(temp, node.text, False, word_num))
            temp = 'ë¶ë§ˆ?¬?—”?“œë¡? ?¸?•˜?—¬ ì´ˆê¸°?™”?¨'
            out_process('-'*10 + '?–‰? ¬ì¢…ë£Œ' + '-'*10)
        print(node.tag) # ?””ë²„ê·¸