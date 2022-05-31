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
        pass
    if (check[1]):
        pass
    if (check[2]):
        pass
    if (check[3]):
        pass
    return "Не удалось определить тип источника"
    

    
        
testStrings = (
    "1. Первушкин, В. И. Губернские статистические комитеты и провинциальная историческая наука / В. И. Первушкин. – Пенза: ПГПУ, 2007. – 214 с.",
    "99. Ставицкий, В. В. Неолит – ранний энеолит лесостепного Посурья и Прихоперья / В.В. Ставицкий, А.А. Хреков. – Саратов: Изд-во Сарат. ун-та, 2003 (Тип. Изд-ва). – 166 с.",
    "155. Кравцова Н.А. Актуальные проблемы современной психосоматики // Человек и современный мир. – 2018. – № 11 (24). – С. 3-10.",
    "122. Оформление списка литературы проектной работы [Электронный ресурс]. – URL: https://workproekt.ru/oformlenie-proekta/oformlenie-spiska-literaturyi/ (дата обращения: 31.05.2022)."
)

testArr = (
    biblio(testStrings[0]),
    biblio(testStrings[1]),
    biblio(testStrings[2]),
    biblio(testStrings[3]),
)