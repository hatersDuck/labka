
"""
    [0] - Книга
    [1] - Интернет-ресурс
    [2] - Закон, нормативный акт и т.п.
    [3] - Статья
"""
import re
import urllib.request
class biblio(object):
    def __init__(self, sourse):
        
        self.type = [
            1,1,1,1
        ]
        self.sourse = sourse
        text = sourse.split()
        self.number = re.match(r"\d{1,}\.",sourse)[0]
        self.fails = []

        if (self.number is None):
            self.fails.append("Не правильно оформленна нумерация")
            self.number = '-1.'

        if (re.search("\s{2,}", sourse) is not None):
            self.fails.append(f"Два и более пробела в одном месте")
            self.sourse.replace("  ", " ")
        
        #############################################
        # Выявление типа                            #
        # Сделанно чересчур просто, много проблем,  #
        # необходимо найти более эффективный способ #
        #############################################

        if (re.search(r"–(\s\d{1,})*\sс\.\s*", sourse.lower()) is None):
            for i in (0, 3): self.type[i] = 0
            # Мало эффективный способ
            if (sourse.lower().find('закон') > 0 or sourse.lower().find('приказ') > 0):
                self.type[1] = 0
            else: self.type[2] = 0
        else:
            for i in (1,2): self.type[i] = 0
            if (sourse.find(' // ') > 0):
                self.type[0] = 0
            if (text[-1] == 'с.'):
                self.type[3] = 0

        for i in (1,2): #Для быстрой остановки инициализации
            if (sum(self.type) > 1 or not(any(self.type))):
                self.type = None
                break
            if (self.type[0]):
                self.type = "Книга"
                self.__book()
                break

            if (self.type[1]):
                self.type = "Интернет-ресурс"
                break

            if (self.type[2]):
                self.type = "Закон, нормативный акт и т.п."
                break

            if (self.type[3]):
                self.type = "Статья в журнале, газете и т.п."
                break
                
    def getFails(self)->str:
        num = f"{self.number}\t"
        if (len(self.fails) == 0 and isinstance(self.type, str)):
            return num + f"Ошибок не найдено"
        elif (len(self.fails) == 0):
            return num + "Не удалось определить тип"
        return num + "\n\t".join(self.fails)

    def __str__(self) -> str:
        msg = ""
        for i in self.__dict__:
            match i:
                case "type":
                    msg += f"Тип: {self.type}\n"
                case "number":
                    msg += f"№{self.number[:-1]}\n"
                case "fails":
                    pass
                case "age":
                    msg += f"{self.type} написана в {self.age[0][2:]} г.\n"
                case "title":
                    msg += f"Название:{self.title}"

        return msg

    ######################
    #Блок проверок типов #
    ######################
    def __checkFIO(self, templateFIO, start = 0) -> None:
        authors = []
        check = start
         
        while(True):
            for i in range(len(templateFIO)):
                temp = re.search(templateFIO[i], self.sourse[start:-1])
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
            self.fails.append("У книги должен быть автор или Фамилия И.О. записаны не правильно")
        if (self.sourse[0:start].count(',') != len(authors) - 1):
            self.fails.append("Между фамилиями должны быть запятые")
        if (len(authors) > 3):
            if (self.sourse.find("и др.") < 0):
                self.fails.append("Если авторов более 3-х, то отмечают первых трёх, затем пишется [и др.] или просто 'и др.'")
        return start

    def __book (self):
        text = self.sourse.split()
        if (self.sourse[self.sourse.find('.') + 1] != ' '):
            self.fails.append("Пробел после {text[0]} обязателен")
        
        start = self.__checkFIO(["[А-Я][а-я]+\s[А-Я]\.\s[A-Я]\.", "[А-Я][а-я]+\s[А-Я]\.[A-Я]\.", "[А-Я][а-я]+\s[А-Я]\."], re.match(r"\d{1,}\.", self.sourse).span()[1])

        template = ',\s\d{4}(?=\.\s[\-–]|\s[(])'
        self.age = re.search(template, self.sourse)
        pages = re.search("\.\s[\-–]\s\d{1,}\s",self.sourse[self.age.span()[0]:-1])
        if (pages is None):
            self.fails.append("Страницы указаны не верно")
        if (self.age is None):
            self.fails.append("Не указан или не правильно оформлен год выпуска")
        self.title = self.sourse[start:self.age.span()[0]]
        city = self.title[self.title.rfind('. -') if (self.title.rfind('. -')>0) else self.title.rfind('. –'):len(self.title)]
        cityReduce = {
            'Москва': 'М.',
            'Ленинград':'Л.', 
            'Санкт-Петербург':'СПб', 
            'Нижний Новгород':"Н. Новогород", 
            'Ростов-на-Дону':"Ростов н/Д"
        }
        for i in cityReduce:
            if (city.find(i) > 0):
                self.fails.append(f"{i} необходимо сократить до {cityReduce[i]}")
        if (city == "" or city.find(':') < 0):
            self.fails.append("Место издания должно быть указано корректно")
        
        self.title = self.title.replace(city, '')
        check = True
        if (self.title.rfind('/ Под ред.') > 0):
            start = self.__checkFIO(["[А-Я]\.\s[A-Я]\.\s[А-Я][а-я]+", "[А-Я]\.[A-Я]\.\s[А-Я][а-я]+"], start = self.sourse.find('/ Под ред.') + len('/ Под ред.'))
            check = False
        if (self.title.rfind(':') > 0):
            publish = ['учебник', "монография", "учеб. пособие"]
            if not(publish[0] in self.title or publish[1] in self.title or publish[2] in self.title):
                self.fails.append("Тип книги {publish} не найден")
            check = False
        if (check):
           self.fails.append("Название или издательство записаны неверно")


    def __checkURL(self):
        dataCall = re.search("[(]дата обращения: \d{2}\.\d{2}\.\d{4}[)].", fullText)
        if (dataCall is None):
            return "Дата обращения не найдена или оформлена не правильно", ""
        template = ".\s[-–]\sURL: (?P<url>https?://[^\s]+)"
        fullURL = re.search(template,fullText)
        if (fullURL is not None):
            URL = fullURL.group("url")
        try:
            urllib.request.urlopen(URL).getcode()
        except:
            return f"Сайт не доступен в данный момент либо указан неверно", ""
        fullText = fullText.replace(fullURL[0] + " " + dataCall[0],"")
        return None, fullText


    def __internetRes(self, sourse: str):
        num = sourse[0:sourse.find('.')]
        exc, sourse = self.__checkURL(sourse)
        if (exc is not None):
            return num + "\t" + exc
        #Не проверяется название.
        return f"{num}\tОформлен в соответсвие с правилами"


# « »  
    
    

testStrings = (
    "1. Первушкин В. И. Губернские статистические комитеты и провинциальная историческая наука / Под ред. В. И. Первушкин. – Пенза: ПГПУ, 2007. – 214 с.",
    "99. Ставицкий В. В. Неолит – ранний энеолит лесостепного Посурья и Прихоперья / Под ред. В.В. Ставицкий, А.А. Хреков. – Саратов: Изд-во Сарат. ун-та, 2003 (Тип. Изд-ва). – 166 с.",
    "155. Кравцова Н. А. Актуальные проблемы современной психосоматики // Человек и современный мир. – 2018. – № 11 (24). – С. 3-10.",
    "122. Оформление списка литературы проектной работы [Электронный ресурс]. – URL: https://wokproekt.ru/oformlenie-proekta/oformlenie-spiska-literaturyi/ (дата обращения: 31.05.2022).",
    "22. Апажева С.С., Баразбиев М., Геграев Х.К. Организация досуга молодежи: учебник. – Нальчик: КБГУ им. Х.М. Бербекова, 2017. – 134 с."
)

testArr = (
    print(biblio(testStrings[0])),
    print(biblio(testStrings[1])),
    print(biblio(testStrings[2])),
    print(biblio(testStrings[3])),
    print(biblio(testStrings[4]))
)