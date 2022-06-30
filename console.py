from antiplagiatAPI import clientAPI
from errors import errors
from biblio import biblio
from find_biblio import find_biblio

conAPI = clientAPI.fromCFG("API_access_1")
while (True):
    path = input("Введите полный путь до файла (docx): ")
    try:
        open(path)
        print()
        for i, err in enumerate(errors(path)):
            print(err)
        bibliosCheck = []
        for i, txt in enumerate(find_biblio(path)):
            if (i == 0):
                continue
            bibliosCheck.append(biblio(txt))
            print(bibliosCheck[i-1])
        print(f"Процент плагиата: {conAPI.simple_check(path):.2f}%")
        print()
    except FileNotFoundError:
        print("Файл не найден")