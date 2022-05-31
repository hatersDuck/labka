
"""
    [0] - Книга
    [1] - Интернет-ресурс
    [2] - Закон, нормативный акт и т.п.
    [3] - Статья
"""
def biblio(sourse: str) -> str: 
    check = [
        1,1,1,1
    ]

    text = sourse.split()
    number = (text[0] if (text[0][0:4].find('.')>0) else None)

    if (number is None):
        return "Не правильно оформленна нумерация"

    if ("".join(i for i in text[-1:-3:-1] if i.upper() == 'С.') == ""):

        for i in (0, 3): check[i] = 0
        if (sourse.lower().find('закон') > 0 or sourse.lower().find('приказ') > 0):
            check[1] = 0
        else: check[2] = 0

    else:
        for i in (1,2): check[i] = 0
      
        if (sourse.find(' // ') > 0):
            check[0] = 0
        if (text[-1] == 'с.'):
            check[3] = 0
    if (check[0]):
        return book(sourse)
    if (check[1]):
        pass
    if (check[2]):
        pass
    if (check[3]):
        pass
    return number + " не удалось определить тип источника"


import pymorphy2
import re
def book (sourse: str):
    morph = pymorphy2.MorphAnalyzer(lang='ru')
    text = sourse.split()
    sourse = sourse[sourse.find('.') + 1:-1]
    
    
    templateName = ["\w+\s[А-ЯЁ]\.\s[A-ЯЁ]\.", "\w+\s[А-ЯЁ]\.[A-ЯЁ]\."] #Фамилия И. О. или Фамилия И.О.
    templates = [
        [templateName[0], templateName[1]], 
        [templateName[0] + ',', templateName[1] + ',']
    ]
    templates.append([
        templates[1][0] + "\s" + templates[0][0],
        templates[1][1] + "\s" + templates[0][1]
        ])
    templates.append([
        templates[1][0] + "\s" + templates[1][0] + "\s" + templates[0][0], 
        templates[1][1] + "\s" + templates[1][1] + "\s" + templates[0][1]
        ])

    authors = []
    temp = 0
    for i, patt in enumerate(templates):
        authors.append(re.search(patt[0], sourse) if re.search(patt[0], sourse) is not None else re.search(patt[1], sourse))
        if (authors[i] is not None):
            if (authors[i].span()[0] != 1):
                return "Ошибка в записи '{text[0]} Фамилия И.О.'"
        if (authors[i] is None): temp += 1
    if (temp > 3): return text[0] + " ошибка в записи Фамилия И.О."
    name = sourse.find("и др.", authors[4].span()[1])

    
        
testStrings = (
    "1. Первушкин В. И. Губернские статистические комитеты и провинциальная историческая наука / В. И. Первушкин. – Пенза: ПГПУ, 2007. – 214 с.",
    "99.  Ставицкий В. В.  Неолит – ранний энеолит лесостепного Посурья и Прихоперья / В.В. Ставицкий, А.А. Хреков. – Саратов: Изд-во Сарат. ун-та, 2003 (Тип. Изд-ва). – 166 с.",
    "155. Кравцова Н. А. Актуальные проблемы современной психосоматики // Человек и современный мир. – 2018. – № 11 (24). – С. 3-10.",
    "122. Оформление списка литературы проектной работы [Электронный ресурс]. – URL: https://workproekt.ru/oformlenie-proekta/oformlenie-spiska-literaturyi/ (дата обращения: 31.05.2022).",
    "22. Апажева С.С., Баразбиев М.И., Геграев Х.К. Организация досуга молодежи: учебник. – Нальчик: КБГУ им. Х.М. Бербекова, 2017. – 134 с."
)

testArr = (
    print(biblio(testStrings[0])),
    print(biblio(testStrings[1])),
    print(biblio(testStrings[2])),
    print(biblio(testStrings[3])),
    print(biblio(testStrings[4]))
)