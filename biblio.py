
"""
    [0] - Книга
    [1] - Интернет-ресурс
    [2] - Закон, нормативный акт и т.п.
    [3] - Статья
"""
import re
def biblio(sourse: str) -> str: 
    check = [
        1,1,1,1
    ]
    #Не идеальный алгоритм надо менять сто проц
    text = sourse.split()
    number = (text[0] if (text[0][0:4].find('.')>0) else None)
    if (number is None):
        return "Не правильно оформленна нумерация"
    if (re.search("\s{2,}", sourse) is not None):
        return f"{number}\tДва и более пробела в одном месте не уместны"

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
    return f"{number}\tНе удалось определить тип источника"


import pymorphy2

def book (sourse: str):
    morph = pymorphy2.MorphAnalyzer(lang='ru')
    text = sourse.split()
    if (sourse[sourse.find('.') + 1] != ' '):
        return f"{text[0]}\tПробел после {text[0]} обязателен"
    sourse = sourse[sourse.find('.') + 2:-1]
    
    
    templateFIO = ["[А-Я][а-я]+\s[А-Я]\.\s[A-Я]\.", "[А-Я][а-я]+\s[А-Я]\.[A-Я]\.", "[А-Я][а-я]+\s[А-Я]\."] #Фамилия И. О. или Фамилия И.О. или Фамилия И.
    authors = []
    start = 0
    check = 0
    while(True):
        for i in range(len(templateFIO)):
            temp = re.search(templateFIO[i], sourse[start:-1])
            if (temp is not None):
                if (temp.span()[0] > 2):
                    continue
                authors.append(temp[0])
                start += temp.span()[1]
                break
        if (check == start):
            break
        else: check = start

    if (len(authors) == 0):
        return f"{text[0]}\tУ книги должен быть автор или Фамилия И.О. записаны не правильно"
    if (sourse[0:start].count(',') != len(authors) - 1):
        return f"{text[0]}\tМежду фамилиями должны быть запятые"
    if (len(authors) > 3):
        if (sourse.find("и др.") < 0):
            return f"{text[0]}\t Если авторов более 3-х, то отмечают первых трёх, затем пишется [и др.] или просто 'и др.'"

    template = ',\s\d{4}(?=\.\s[\-–]|\s[(])'
    age = re.search(template, sourse)

    if (age is None):
        return f"{text[0]}\tНе указан или не правильно оформлен год выпуска"
    
    title = sourse[start:age.span()[0]]
    city = title[title.rfind('. -') if (title.rfind('. -')>0) else title.rfind('. –'):len(title)]

    if (city == ""):
        return f"{text[0]}\tМесто издания должно быть указано корректно"
    
    title = title.replace(city, '')
    if (sourse.find('/') > 0):
        pass
    else:
        pass


# « »  
    
    

testStrings = (
    "1. Первушкин В. И. Губернские статистические комитеты и провинциальная историческая наука / В. И. Первушкин. – Пенза: ПГПУ, 2007. – 214 с.",
    "99. Ставицкий В. В. Неолит – ранний энеолит лесостепного Посурья и Прихоперья / В.В. Ставицкий, А.А. Хреков. – Саратов: Изд-во Сарат. ун-та, 2003 (Тип. Изд-ва). – 166 с.",
    "155. Кравцова Н. А. Актуальные проблемы современной психосоматики // Человек и современный мир. – 2018. – № 11 (24). – С. 3-10.",
    "122. Оформление списка литературы проектной работы [Электронный ресурс]. – URL: https://workproekt.ru/oformlenie-proekta/oformlenie-spiska-literaturyi/ (дата обращения: 31.05.2022).",
    "22. Апажева С.С., Баразбиев М., Геграев Х.К. Организация досуга молодежи: учебник. – Нальчик: КБГУ им. Х.М. Бербекова, 2017. – 134 с."
)

testArr = (
    print(biblio(testStrings[0])),
    print(biblio(testStrings[1])),
    print(biblio(testStrings[2])),
    print(biblio(testStrings[3])),
    print(biblio(testStrings[4]))
)