"""
    Объеснение что откуда берётся в файле create.ipynb
"""

templ = {
    'start': [
            "Федеральный\sзакон\s",
            "Приказ\s",
            "Закон\s",
            "[А-Я][а-я]+\sкодекс\s",
            "Указ\sПрезидента\s",
            "Постановление\sПравительства\s",
            "Конституция\s"
        ],
    'from': [
            "Мин[а-я]+\sРоссии\s",
            "Российской\sФедерации\s",
            "[А-Я][а-я]+\s[а-я]+\s" #Тут могло быть описание всех возможных республик, краёв, автономных округов и т.п. Но тут нужен специалист поэтому считаю не обязательным).
        ],
    'date': 
        "от\s\d{2}\.\d{2}\.\d{4}(\s)?",
    'num': 
        "№\s?\d{1,}(\s?\-[А-Я]{1,})?(\s)?",
    'red': 
        "(?<=\()ред.\sот\s\d{2}\.\d{2}\.\d{4}(\s)?.*?(?=\))?",
    'name': 
        "«(?<=«)[А-Я].*?(?=»)»(\s)?",
    'URL': 
        '\[(Электронный\sресурс|сайт)\]\.\s?[-–]\s?URL:\s?(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})\s?\(дата обращения:\s?\d{2}\.\d{2}\.\d{4}\);',
    

    'author': 
        "[А-Я][а-я]+(\s|\,)[А-Я]\.\s?[А-Я]\.\s?(и\sдр\.\s?)?",
    'title': 
        "[А-Я].*?[\.\:/]",
    'type': 
        '\s?((учебник\.)'+
        '|(монография\.)'+
        '|(учеб((\.)|(ное))\sпособие[\.\s](для\sвузов)?))',
    'city': 
        '\s?[\-–]\s?((М\.)|(Л\.)|(СПб\.)|(Н\.\sНовгород)|(Ростов\sн\/Д/.)|([А-Я].*?[\:\s]))',
    'iz': 
        '\:?\s[А-Я].*\,\s',
    'age': 
        '\d{4}\.',
    'page': 
        '\s[\-–]\s?((\d{1,}\sс)|(С\.second\d{1,}))\.',
    'redBook': 
        '/?\s((Под\sред\.)|(Пер\.\sc\s[а-я]+))\s?',           
    'authorRe': 
        '[А-Я]\.[А-Я]\.\s[А-Я][а-я]+\.',
}


def createBib(template):
    temp = "("
    for i in template['start']:
        temp += "(" + i + ')|'
    temp = temp[0:-1] + ")("
    for i in template['from']:
        temp += "(" + i + ')|'
    temp = temp[0:-1] + ")"

    temp += template['date'] + template['num'] + template['red'] + template['name']

    return [
        template['author'] + template['title'] + template['city'] + template['iz'] + template['age'] + template['page'],
        template['author'] + template['title'] + template['type'] + template['city'] + template['iz'] + template['age'] + template['page'],
        template['title'] + template['redBook'] + template['authorRe'] + template['city'] + template['iz'] + template['age'] + template['page'],
        temp
    ]

import re
import urllib.request
templates = createBib(templ)
class checkBiblio(object):
    
    def __init__(self, sourse):
        self.source = sourse
        self.status = False
        
        number = re.search('\d{1,}[\s,\.]', sourse)
        self.number = number[0] if number else '-1.'

        for j in templates:
            if (re.search(j, sourse)):
                self.status = True
                break
        
        if (re.search(templ['URL'], sourse)):
            pass #urlib.request

    def __repr__(self) -> str:
        return ['Не подходит', 'Подходит'][self.status]    

    def __bool__(self) -> bool:
        return self.status

if __name__ == '__main__':
    test = [
    "Яковлев Ю.Я. Рассказы и повести. – М.: Детская литература, 2018. – 272 с.",
    "Сулейманов Р.Ф. Музыка в нашей жизни: монография. – Казань: Познание, 2018. – 112 с.",
    "Шорникова М.И. Музыкальная литература. Музыка, ее формы и жанры: учеб. пособие. – Ростов н/Д.: Феникс, 2017. – 245 с.",
    "Апажева С.С., Баразбиев М.И., Геграев Х.К. Организация досуга молодежи: учебник. – Нальчик: КБГУ им. Х.М. Бербекова, 2017. – 134 с.",
    "Роль физических упражнений в жизни человека / Под ред. И.В. Светловой. – М.: Перо, 2016. – 318 с."
    ]

    for i, txt in enumerate(test):
        print(f'{i + 1} – {checkBiblio(txt)}')


    
