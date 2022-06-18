import os
import suds
import suds.client
import time
import base64
import urllib
import io
import base64
import sys
import datetime

class dataFile(object):
    def __init__(self, filename, client) -> None:
        self.data = client.factory.create("DocData")
        self.data.Data = base64.b64encode(open(filename, "rb").read()).decode()
        self.data.FileName = os.path.splitext(filename)[0]
        self.data.FileType = os.path.splitext(filename)[1]
        self.data.ExternalUserID = self.data.FileName.split("/")[-1]

# Создать клиента сервиса(https)
class clientAPI(object):
    def __init__(self, login:str, password:str, company_name:str, API_adress:str):
        #Подключение к API
        self.client = suds.client.Client("https://%s/apiCorp/%s?singleWsdl" % (API_adress, company_name),
                                    username=login,
                                    password=password)
    @classmethod
    def fromCFG(cls, access):
        import configparser
        config = configparser.ConfigParser()
        config.read('config.ini', encoding='utf-8-sig')

        APICORP_ADDRESS = config.get(access, "APICORP_ADDRESS").replace('"', "")
        COMPANY_NAME = config.get(access, "COMPANY_NAME").replace('"', "")
        LOGIN = config.get(access, "LOGIN").replace('"', "")
        PASSWORD = config.get(access, "PASSWORD").replace('"', "")
        return cls(LOGIN, PASSWORD, COMPANY_NAME, APICORP_ADDRESS)

    def simple_check(self, filename):
        print("SimpleCheck filename=" + filename)
        # Описание загружаемого файла
        data = dataFile(filename, self.client).data

        docatr = self.client.factory.create("DocAttributes")
        personIds = self.client.factory.create("PersonIDs")
        personIds.CustomID = "original"

        arr = self.client.factory.create("ArrayOfAuthorName")

        author = self.client.factory.create("AuthorName")
        author.OtherNames = "Иван Иванович"
        author.Surname = "Иванов"
        author.PersonIDs = personIds

        arr.AuthorName.append(author) 
        
        docatr.DocumentDescription.Authors = arr

        # Загрузка файла
        try:
            uploadResult = self.client.service.UploadDocument(data, docatr)
        except Exception:
            raise

        # Идентификатор документа. Если загружается не архив, то список загруженных документов будет состоять из одного элемента.
        id = uploadResult.Uploaded[0].Id

        try:
            # Отправить на проверку с использованием всех подключеных компании модулей поиска
            self.client.service.CheckDocument(id)
            # Отправить на проверку с использованием только собственного модуля поиска и модуля поиска "wikipedia". Для получения списка модулей поиска см. пример get_tariff_info()
            #client.service.CheckDocument(id, ["wikipedia", COMPANY_NAME])
        except suds.WebFault:
            raise

        # Получить текущий статус последней проверки
        status = self.client.service.GetCheckStatus(id)

        # Цикл ожидания окончания проверки
        while status.Status == "InProgress":
            time.sleep(status.EstimatedWaitTime*0.1)
            status = self.client.service.GetCheckStatus(id)

        # Проверка закончилась не удачно.
        if status.Status == "Failed":
            print(u"При проверке документа %s произошла ошибка: %s" % (filename, status.FailDetails))

        # Получить краткий отчет
        report = self.client.service.GetReportView(id)

        print("Report Summary: %0.2f%%" % (report.Summary.Score,))
        for checkService in report.CheckServiceResults:
            # Информация по каждому поисковому модулю
            print("Check service: %s, Score.White=%0.2f%% Score.Black=%0.2f%%" %
                    (checkService.CheckServiceName,
                    checkService.ScoreByReport.Legal, checkService.ScoreByReport.Plagiarism))
            if not hasattr(checkService, "Sources"):
                continue
            for source in checkService.Sources:
                # Информация по каждому найденному источнику
                print('\t%s: Score=%0.2f%%(%0.2f%%), Name="%s" Author="%s" Url="%s"' %
                    (source.SrcHash, source.ScoreByReport, source.ScoreBySource,
                    source.Name, source.Author, source.Url))

        # Получить полный отчет
        options = self.client.factory.create("ReportViewOptions")
        options.FullReport = True
        options.NeedText = True
        options.NeedStats = True
        options.NeedAttributes = True
        fullreport = self.client.service.GetReportView(id, options)
        if fullreport.Details.CiteBlocks:
            # Найти самый большой блок заимствований и вывести его
            maxBlock = max(fullreport.Details.CiteBlocks, key=lambda x: x.Length)
            print(u"Max block length=%s Source=%s text:\n%s..." % (maxBlock.Length, maxBlock.SrcHash,
                fullreport.Details.Text[maxBlock.Offset:maxBlock.Offset + min(maxBlock.Length, 200)]))
                
        print(u"Author Surname=%s OtherNames=%s CustomID=%s" % (fullreport.Attributes.DocumentDescription.Authors.AuthorName[0].Surname,
            fullreport.Attributes.DocumentDescription.Authors.AuthorName[0].OtherNames,
            fullreport.Attributes.DocumentDescription.Authors.AuthorName[0].PersonIDs.CustomID))
    


API_con1 = clientAPI.fromCFG("API_access_1")
API_con1.simple_check("/home/danila/codes/clones/labka/testFiles/pz2.pdf")