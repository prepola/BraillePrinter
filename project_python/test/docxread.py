# -*- coding: utf-8 -*-
import zipfile, re
import xml.etree.ElementTree as ET

def str_init (str_temp, str_text, bool_row, int_word) :
    if (bool_row == False) & (str_temp != None) :
        return str_temp
    elif (bool_row == True) & (str_temp != None) :
        if (str_temp != '') & (int_word < 2) :
            str_temp = str_temp + ' | ' # ?? κ°? ?? κ΅¬λΆ
    if str_temp == None : return str_text
    str_temp = str_temp + str_text
    return str_temp

def out_process (data) :
    print(data)
    return None

temp = str()
matrix_state = False
row_state = False 
word_num = 0 # κ³΅λ°±?΄ ?? Text Element?? κ³΅λ°±λ¬Έμκ°? ?½??? κ²μ λ°©μ???κΈ? ?? λ³??
file_name = str()
ns = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'

while True :
    try :
        file_name = input('??Όλͺμ ?? ₯??¬ μ£Όμ­??€ :')
        if len(file_name) < 1 : file_name = 'test.docx' # ?λ²κ·Έ
        elif file_name[-5:] != '.docx' : file_name = file_name + '.docx'
        docx = zipfile.ZipFile(file_name)
        context = docx.read('word/document.xml')
    except :
        out_process('?λͺ»λ ?? ??Ό')
        break
    
    tree = context.decode()
    root = ET.fromstring(tree)
    tree_list = root.iter()

    print(tree)

    for node in tree_list:
        if node.tag == ns + 'tr' : # ? κ΅¬λΆ ?κ·?
            matrix_state = True
            if temp != '' : # ? λ§λ¬΄λ¦¬μ temp? ????₯? text μΆλ ₯
                out_process(str_init(temp, node.text, False, word_num))
                temp = 'tr? ??΄? μ΄κΈ°? ?¨'
        elif node.tag == ns + 'tc' : # ?΄ κ΅¬λΆ ?κ·?
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
        elif node.tag == ns + 'bookmarkStart' : # ?? ¬ ?? ?κ·?
            out_process('-'*10 + '?? ¬??' + '-'*10)
        elif node.tag == ns + 'bookmarkEnd': # ?? ¬ μ’λ£ ?κ·?
            matrix_state = False
            row_state = False
            out_process(str_init(temp, node.text, False, word_num))
            temp = 'λΆλ§?¬??λ‘? ?Έ??¬ μ΄κΈ°??¨'
            out_process('-'*10 + '?? ¬μ’λ£' + '-'*10)
        print(node.tag) # ?λ²κ·Έ