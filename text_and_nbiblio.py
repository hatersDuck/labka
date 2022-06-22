from docx import Document
import docx2txt
import re

def text_and_nbiblio(way):
    my_text = docx2txt.process(way)
    str = my_text.splitlines()
    i = 0
    zagl = []
    flg = 0
    while (i < len(str)):
        if (flg == 1):
            if ('Заключение'.lower() in str[i].lower()):
                zagl.append(re.sub("[0-9]+|[\.]", "", str[i].lower()).strip())
                break
            if (str[i] != ''):
                zagl.append(re.sub("[0-9]+|[\.]", "", str[i].lower()).strip())    
        if (re.sub("[0-9]+|[\.]", "", str[i].lower()).strip() == 'Введение'.lower()):
            flg = 1
        i = i + 1
    document = Document(way)
    num_abzac = 0
    abz = ''
    temp = ''
    j = 0
    text_biblio = []
    for paragraph in document.paragraphs:
        if (zagl[num_abzac] == re.sub("[0-9]+|[\.]", "", paragraph.text).strip().lower()):
            num_abzac = num_abzac+1
            if (num_abzac >= len(zagl)):
                break
        elif (num_abzac != 0):
            abz = abz+paragraph.text
            i = 0
            while i < len(abz):
                if abz[i] == '[':
                    bool = 1
                    text_biblio.append(['',''])
                    text_biblio[j][1] = temp
                    print(temp)
                    temp = ''
                elif abz[i] == ']':
                    bool = 0
                    text_biblio.append(['',''])
                    text_biblio[j][0] = temp
                    print(temp)
                    j = j+1
                    temp = ''
                    i = i+1
                else:
                    temp = temp+abz[i]
                i = i+1
            abz = ''
    return text_biblio      #порядок данных в двумерном массиве: Ссылка на источник (номер), Текст

#######
#r = 'd:/Сибгути/1 курс/Экономика/Курсовая Дефицит бюджета (ИИ-051 Носков Кирилл).docx'
r = 'd:/РГЗ Вариант 13 (ИИ-051 Носков Кирилл).docx'
end = text_and_nbiblio(r)
#print(end)

    