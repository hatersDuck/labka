
"""
    [0] - Книга
    [1] - Интернет-ресурс
    [2] - Закон, нормативный акт и т.п.
    [3] - Статья
"""
import re
from tabnanny import check
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

def checkFio(sourse, templateFIO, num, start = 0):
    authors = []
    check = start
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
        return f"{num}\tУ книги должен быть автор или Фамилия И.О. записаны не правильно"
    if (sourse[0:start].count(',') != len(authors) - 1):
        return f"{num}\tМежду фамилиями должны быть запятые"
    if (len(authors) > 3):
        if (sourse.find("и др.") < 0):
            return f"{num}\t Если авторов более 3-х, то отмечают первых трёх, затем пишется [и др.] или просто 'и др.'"
    return None, start, authors

def book (sourse: str):
    text = sourse.split()
    if (sourse[sourse.find('.') + 1] != ' '):
        return f"{text[0]}\tПробел после {text[0]} обязателен"
    sourse = sourse[sourse.find('.') + 2:-1]
    
    exc, start = checkFio(sourse, ["[А-Я][а-я]+\s[А-Я]\.\s[A-Я]\.", "[А-Я][а-я]+\s[А-Я]\.[A-Я]\.", "[А-Я][а-я]+\s[А-Я]\."], text[0])
    if (exc is not None):
        return exc
    template = ',\s\d{4}(?=\.\s[\-–]|\s[(])'
    age = re.search(template, sourse)
    pages = re.search("\.\s[\-–]\s\d{1,}\s",sourse[age.span()[0]:-1])
    if (pages is None):
        return f"{text[0]}\tСтраницы указаны не верно"
    if (age is None):
        return f"{text[0]}\tНе указан или не правильно оформлен год выпуска"
    title = sourse[start:age.span()[0]]
    city = title[title.rfind('. -') if (title.rfind('. -')>0) else title.rfind('. –'):len(title)]
    cityReduce = {
        'Москва': 'М.',
        'Ленинград':'Л.', 
        'Санкт-Петербург':'СПб', 
        'Нижний Новгород':"Н. Новогород", 
        'Ростов-на-Дону':"Ростов н/Д"
    }
    for i in cityReduce:
        if (city.find(i) > 0):
            return f"{text[0]}\t{i} необходимо сократить до {cityReduce[i]}"
    if (city == "" or city.find(':') < 0):
        return f"{text[0]}\tМесто издания должно быть указано корректно"
    
    title = title.replace(city, '')
    check = True
    if (title.rfind('/ Под ред.') > 0):
        exc, start = checkFio(title, ["[А-Я]\.\s[A-Я]\.\s[А-Я][а-я]+", "[А-Я]\.[A-Я]\.\s[А-Я][а-я]+"], text[0], start = title.rfind('/ Под ред.') + len('/ Под ред.'))
        if (exc is not None):
            return exc
        check = False
    if (title.rfind(':') > 0):
        publish = ['учебник', "монография", "учеб. пособие"]
        if not(publish[0] in title or publish[1] in title or publish[2] in title):
            return f"{text[0]}\tТип книги {publish} не найден"
        check = False
    if (check):
        return f"{text[0]}\tНазвание или издательство записаны неверно"
    



# « »  
    
    

testStrings = (
    "1. Первушкин В. И. Губернские статистические комитеты и провинциальная историческая наука / Под ред. В. И. Первушкин. – Пенза: ПГПУ, 2007. – 214 с.",
    "99. Ставицкий В. В. Неолит – ранний энеолит лесостепного Посурья и Прихоперья / Под ред. В.В. Ставицкий, А.А. Хреков. – Саратов: Изд-во Сарат. ун-та, 2003 (Тип. Изд-ва). – 166 с.",
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