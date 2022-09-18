from docx import Document
import docx2txt
import re
from PyPDF2 import PdfFileReader
from docx2pdf import convert
import os

def errors(way):
    my_text = docx2txt.process(way)
    str = my_text.splitlines()
    i = 0
    base_errors = [0,0,0,0,0] #содержание, введение, заключение, список литературы
    text_errors = ['содержание', 'введение', 'заключение', 'список литературы', 'cписок использованных источников']
    zagl = []
    errors = []
    flg = 0
    k = 0
    while (i < len(str)):
        txt = re.sub("[0-9]+|[\.]", "", str[i].lower()).strip()
        j = 0
        while (j < len(text_errors)):
            if (txt == text_errors[j]):
                base_errors[j] = base_errors[j]+1
                flg = 1
            j = j+1
        if (txt in zagl):
            k = k+1
        if (base_errors[1] == 2):
            flg = 2
        if (flg == 1):
            if (txt != ''):
                zagl.append(txt) 
        i = i+1
    flg = 0
    if (k+1 != len(zagl)):
        flg = 1   

    i = 0
    while (i < len(base_errors)-1): #### ошибки ключевых заголовков
        if (i == 0):
            if (base_errors[i] == 0):
                flg = 1
        elif (i < 3):
            if (base_errors[i] < 2):
                flg = 1
        else:
            if (base_errors[i] != 2) and (base_errors[i+1] != 2):
                flg = 1
        i = i+1
    if (flg == 1):
        errors.append('Ошибка в заголовках или содержании')

    document = Document(way)
    sections = document.sections
    len(sections)
    flg = 1
    s = ['','']
    for section in sections:
        if ((round(section.top_margin.cm, 2) != 2) or (round(section.bottom_margin.cm, 2) != 2) 
        or (round(section.left_margin.cm, 2) != 3) or (round(section.right_margin.cm, 2) != 1)):
            flg = 0
        if (section.footer.is_linked_to_previous == True):
            s[0] = 1
        if (section.footer.is_linked_to_previous != True):
            s[1] = 1
        
    if flg == 0:
        errors.append('Неправильные поля')
    if (s[0] != 1 or s[1] != 1):
        errors.append('Ошибка в нумерации')
       
    flg = 0
    for paragraph in document.paragraphs:
        a = 0
        b = 0
        if flg == 1:
            for r in paragraph.runs:
                if (r.font.size.pt != 14):
                    a = 1
                if (r.font.name != None) and (r.font.name != 'Times New Roman'):
                    b = 1

            if (paragraph.paragraph_format.line_spacing != 1.5):
                errors.append('Неверный межстрочный интервал')
            if (a == 1):
                errors.append('Неверный размер шрифта')
            if (b == 1):
                errors.append('Неверный шрифт') 
            break
        if (paragraph.text.strip().lower() == 'введение'):
            flg = 1
    return errors

def num_pages(way):
    temp_pdf = os.path.dirname(way)+'temp.pdf'
    convert(way, temp_pdf)
    with open(temp_pdf, "rb") as filehandle:  
        pdf = PdfFileReader(filehandle)
        pages = pdf.getNumPages()
        return (pages) 
    os.remove(temp_pdf)

def student_group(way):
    my_text = docx2txt.process(way)
    str = my_text.splitlines()
    text = ['Выполнил:', 'Группа:', 'гр.', 'введение']
    i = 0
    res = []
    while (i < len(str)):
        txt = str[i]
        if (text[0] in txt):
            v = (re.sub(f'{text[0]}', "", str[i]).strip()).split(' ')
            v = v[0]+' '+v[1][0]+'. '+v[2][0]+'.'
            res.append(v)
        elif (text[1] in txt):
            v = re.sub(f'{text[1]}+|{text[2]}', "", str[i]).strip()
            res.append(v)
        elif (text[2] in txt):
            v = txt.partition(f'{text[2]}')[2].strip()
            res.append(v)
        if (txt.lower().split == text[3]):
            break
        i = i+1
    return res
            

r = 'd:/РГЗ Вариант 13 (ИИ-051 Носков Кирилл).docx'
#r = 'd:/Сибгути/1 курс/Экономика/Курсовая Дефицит бюджета (ИИ-051 Носков Кирилл).docx'

fg = student_group(r)
if fg != []:
    print (fg)
#num_pages(r)