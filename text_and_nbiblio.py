from docx import Document
import docx2txt
import re

def text_and_nbiblio(way):
    my_text = docx2txt.process(way)
    str = my_text.splitlines()
    i = 0
    zagl = []
    flg = 0
    while (i < len(str)): #(flg != 2) or 
        if (flg == 1):
            if ('Заключение' in str[i]):
                zagl.append(re.sub("[0-9]+|[\.]", "", str[i]).strip())
                break
            if (str[i] != ''):
                zagl.append(re.sub("[0-9]+|[\.]", "", str[i]).strip())    
        if (re.sub("[0-9]+|[\.]", "", str[i]).strip() == 'Введение'):
            flg = 1
        i = i + 1
    document = Document(way)
    num_abzac = 0
    abz = ''
    temp = ''
    text_biblio = []
    for paragraph in document.paragraphs:
        if (zagl[num_abzac] == re.sub("[0-9]+|[\.]", "", paragraph.text).strip()):
            num_abzac = num_abzac+1
            if (num_abzac >= len(zagl)):
                break
        elif (num_abzac != 0):
            abz = abz+paragraph.text
            i = 0
            while i < len(abz):
                if abz[i] == '[':
                    bool = 1
                    text_biblio.append(temp)
                    temp = ''
                elif abz[i] == ']':
                    bool = 0
                    text_biblio.append(temp)
                    temp = ''
                    i = i+1
                else:
                    temp = temp+abz[i]
                i = i+1
            abz = ''
    return text_biblio      #порядок данных: Текст, Номер источника

#######
r = 'd:/Сибгути/1 курс/Экономика/Курсовая Дефицит бюджета (ИИ-051 Носков Кирилл).docx'
end = text_and_nbiblio(r)   #можно переделать на двумерный массив возвращающиеся данные 
print(end)

    