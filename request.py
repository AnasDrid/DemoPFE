from __future__ import print_function
from datetime import date
import time
from supabase import create_client, Client
import dateparser
import random
import re
import urllib
from pprint import pprint
import requests
from requests.structures import CaseInsensitiveDict
from bs4 import BeautifulSoup
from datetime import datetime
import locale
import httplib2
import os
import io
import re
from apiclient import discovery
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
from oauth2client.file import Storage
from apiclient import http
import json
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.layout import LAParams
from pdfminer.converter import TextConverter
from io import StringIO
from pdfminer.pdfpage import PDFPage
from pdf2image import convert_from_path
from PIL import Image
from oauth2client import client
from oauth2client import tools
import PyPDF2
from elastic_enterprise_search import AppSearch
import requests
requests.packages.urllib3.disable_warnings()
import ssl
import smtplib
from email.message import EmailMessage

def prepArab(client):
    url = "https://www.joradp.dz/SCRIPTS/JOA_Rec.dll/OptPost"
    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "text/plain"
    data = f"Client={client}&dref=o&dsom=o&ddec=o&daff=200&dtri=0+%3A+%C7%E1%D1%DE%E3&dOri=r"
    resp = requests.post(url, headers=headers, data=data,verify = False)

def prepFrancais(client):
    url = "https://www.joradp.dz/SCRIPTS/JOF_Rec.dll/OptPost"
    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "text/plain"
    data = f"Client={client}&dref=o&dsom=o&ddec=o&daff=200&dtri=0+%3A+%C7%E1%D1%DE%E3&dOri=r"
    resp = requests.post(url, headers=headers, data=data,verify = False)

def getArab(Numero,annee):
    client=random.randint(3500,3600)
    prepArab(client)
    url = "https://www.joradp.dz/SCRIPTS/Joa_Rec.dll/RecPost"

    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "text/plain"

    data =  f"Client={client}&Start=0&zsec=&zmin=&znat=&znjo={Numero}&znjd=01%2F01%2F{annee}&znjf=31%2F12%2F{annee}&zntx=&zntd=&zntf=&zdes=&ztyp=2"


    resp = requests.post(url, headers=headers, data=data,verify = False)
    resp.encoding="1256"
    print(resp.text)
    return resp.text


def getFrench(num,annee):
    client = random.randint(3500, 3600)
    prepFrancais(client)
    print("client:" +str(client))
    url = "https://www.joradp.dz/SCRIPTS/Jof_Rec.dll/RecPost"
    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "text/plain"
    data = f"Client={client}&Start=0&zsec=&zmin=&znat=&znjo={num}&znjd=01%2F01%2F{annee}&znjf=31%2F12%2F{annee}&zntx=&zntd=&zntf=&zdes=&ztyp=2"
    resp = requests.post(url, headers=headers, data=data,verify = False)
    print(resp.text)
    return resp.text



def testarab():
    html=getArab(29,2022)
    soup = BeautifulSoup(html, 'html.parser')

    tab=soup.find_all("tr")
    tab.pop(0)
    tab.pop(0)
    tab.pop()
    print("arabe")
    for t in tab:
        print(t)

def testFrench():
    html = getFrench()

    soup = BeautifulSoup(html, 'html.parser')

    tab = soup.find_all("tr")
    tab.pop(0)
    tab.pop(0)
    tab.pop()
    print("francais")
    for t in tab:
        print(t)

    return tab

class Final:
    def __init__(self):
     self.file_name_ar=None
     self.ministry_ar=None
     self.title_ar=None
     self.page_ar=None
     self.type_text_ar=None
     self.text_ar=None
     self.sectors_ar=None
     self.keywords_ar=None
     self.file_name_fr=None
     self.ministry_fr=None
     self.title_fr=None
     self.page_fr=None
     self.type_text_fr=None
     self.text_fr=None
     self.sectors_fr=None
     self.keywords_fr=None
     self.date=None
     self.year=None
     self.rechercheAR=None
     self.rechercheFR=None
     self.error=False

class Result:
    def __init__(self,file_name_ar,ministry_ar,title_ar,page_ar,type_text_ar,text_ar,sectors_ar,keywords_ar,file_name_fr,ministry_fr,title_fr,page_fr,type_text_fr,text_fr,sectors_fr,keywords_fr,date,year,error):
     self.file_name_ar=file_name_ar
     self.ministry_ar=ministry_ar
     self.title_ar=title_ar
     self.page_ar=page_ar
     self.type_text_ar=type_text_ar
     self.text_ar=text_ar
     self.sectors_ar=sectors_ar
     self.keywords_ar=keywords_ar
     self.file_name_fr=file_name_fr
     self.ministry_fr=ministry_fr
     self.title_fr=title_fr
     self.page_fr=page_fr
     self.type_text_fr=type_text_fr
     self.text_fr=text_fr
     self.sectors_fr=sectors_fr
     self.keywords_fr=keywords_fr
     self.date_publication_fr=date
     self.year_jo=year
     self.error=error
     self.id=None

class pretraitement:
    def __init__(self,t1,t2,t3,t4):
        self.text1=t1
        self.text2=t2
        self.text3=t3
        self.text4=t4

class pretraitementar:
    def __init__(self,t1,t2,t3,t4):
        self.text1=t1
        self.text2=t2
        self.text3=t3
        self.text4=t4


def getdataFrancais(num,annee):
    html = getFrench(num,annee)
    soup = BeautifulSoup(html, 'html.parser')
    tab = soup.find_all("tr")
    tab.pop(0)
    tab.pop(0)
    tab.pop()
    return tab

def getdataArabe(num,annee):
    html = getArab(num, annee)
    soup = BeautifulSoup(html, 'html.parser')
    tab = soup.find_all("tr")
    tab.pop(0)
    tab.pop(0)
    tab.pop()
    return tab

def repartition(tab):
    cpt = 0
    ttab = []
    temp = []
    lim="[D&eacutetail]"
    limar="[التفاصيل]"
    for t in tab:
        print(t.text)
        if lim in t.text or limar in t.text:
            ttab.append(temp)
            temp = []
        temp.append(t)
    ttab.append(temp)
    ttab.pop(0)
    print("size="+str(len(ttab)))
    return ttab

def orgTexts(tab):
    ttab=[]
    for t in tab:
        if(len(t)==4):
            ttab.append(pretraitement(t[1].text, "", t[2].text, t[3].text))
            print("if entered")
        else:
            ttab.append(pretraitement(t[1].text, t[2].text, t[3].text, t[4].text))
    return ttab

def traitement(num,annee):
    Arabe=repartition(getdataArabe(num,annee))
    Francais=repartition(getdataFrancais(num,annee))
    print("francais")
    print(len(Francais))
    Result=[]
    FrancaisOrg=orgTexts(Francais)
    for t in FrancaisOrg:
        obj = Final()
        obj.file_name_ar = genFileAr(num, annee)
        obj.file_name_fr = genFileFr(num, annee)
        obj.ministry_fr = t.text2
        matches = re.finditer("du ", t.text1)
        for m in matches:
            obj.date=t.text1[m.end():]
        obj.title_fr=t.text1+" "+t.text4
        obj.rechercheFR=t.text4
        obj.year=annee
        matches = re.finditer("Page ", t.text3)
        for m in matches:
            obj.page_fr=t.text3[m.end():]
        Result.append(obj)
        obj.type_text_fr=getCat(t.text1)
    cpt=0
    ArabeOrg=orgTexts(Arabe)
    for t in ArabeOrg:
        Result[cpt].title_ar=t.text1+" "+t.text4
        Result[cpt].rechercheAR = t.text4
        Result[cpt].ministry_ar=t.text2
        '''matches = re.finditer("في ", t.text1)
        for m in matches:
            Result[cpt].date = t.text1[m.end():]'''
        matches = re.finditer("الصفحة ", t.text3)
        for m in matches:
            Result[cpt].page_ar = t.text3[m.end():]
        print("\n\nt")
        print(t.text1)
        Result[cpt].type_text_ar=getCat(t.text1)
        cpt+=1
    for r in Result:
        pprint(vars(r))
    return Result

def genFileAr(num,annee):
    if (num>0 and 10>num):
        return f"A{annee}00{num}.pdf"
    elif (num>9 and 100>num):
        return f"A{annee}0{num}.pdf"
    else:return f"A{annee}{num}.pdf"

def genFileFr(num,annee):
    if (num>0 and 10>num):
        return f"F{annee}00{num}.pdf"
    elif (num>9 and 100>num):
        return f"F{annee}0{num}.pdf"
    else:return f"F{annee}{num}.pdf"

def getCat(text):
    List=["أمر",
          "منشور",
          "لائحة",
          "مداولة",
          "مداولة م-أ-للدولة",
          "مرسوم",
          "منشور وزاري مشترك",
          "مرسوم تنفيذي",
          "مرسوم تشريعي",
          "مرسوم رئاسي",
          "مقرر",
          "مقرر وزاري مشترك",
          "إعلان",
          "نظام",
          "اتفاقية",
          "تصريح",
          "تقرير",
          "تعليمة",
          "تعليمة وزارية مشتركة",
          "جدول",
          "رأي",
          "قانون",
          "قرار",
          "قرار ولائي",
          "قرار وزاري مشترك",
          "Arrêté",
          "Arrêté de wali",
          "Arrêté inter",
          "Avis",
          "Barème",
          "Circulaire",
          "Circulaire inter",
          "Convention",
          "Décision",
          "Décision inter",
          "Déclaration",
          "Décret",
          "Décret exécutif",
          "Décret législatif",
          "Décret Présidentiel",
          "Délibération",
          "Délibération du HCE",
          "Instruction",
          "Instruction inter",
          "Loi",
          "Ordonnance",
          "Proclamation",
          "Rapport",
          "Règlement",
          "Résolution"]
    res = [string for string in List if string in text]
    return res[-1]


def get_credentials():

    # If modifying these scopes, delete your previously saved credentials
    # at ~/.credentials/drive-python-quickstart.json
    SCOPES = 'https://www.googleapis.com/auth/drive'
    CLIENT_SECRET_FILE = 'client_secret_395744274280-ot1ar85i1306dvbo7ql1a7rqblc3j1bn.apps.googleusercontent.com.json'
    APPLICATION_NAME = 'Drive API'

    credential_path = os.path.join("./", 'drive-python-quickstart.json')
    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def ocr(file):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)

    imgfile = file+'.jpg'  # Image with texts (png, jpg, bmp, gif, pdf)
    txtfile = file+'.txt'  # Text file outputted by OCR

    mime = 'application/vnd.google-apps.document'
    res = service.files().create(
        body={
            'name': imgfile,
            'mimeType': mime
        },
        media_body=MediaFileUpload(imgfile, mimetype=mime, resumable=True)
    ).execute()

    downloader = MediaIoBaseDownload(
        io.FileIO(txtfile, 'wb'),
        service.files().export_media(fileId=res['id'], mimeType="text/plain")
    )
    done = False
    while done is False:
        status, done = downloader.next_chunk()

    service.files().delete(fileId=res['id']).execute()
    print(f"OCR {imgfile} Done.")

def getSommaireFr(file):
    file1 = open(file, "r", encoding='utf-8')
    count = 0
    lines = file1.readlines()
    pair = True
    for line in lines:
        if (re.search("SOMMAIRE", line)):
            page = lines[count - 7]
            if (pair):
                last = int(page)
                pair = False
            else:
                page = lines[count - 2]
                last = int(page)
                pair = True
        count = count + 1
    file1.close()
    return last

def get_pdf_file_content(path_to_pdf):
    resource_manager = PDFResourceManager(caching=True)
    out_text = StringIO()
    codec = 'utf-8'
    laParams = LAParams()
    text_converter = TextConverter(resource_manager, out_text, laparams=laParams)
    fp = open(path_to_pdf, 'rb')
    interpreter = PDFPageInterpreter(resource_manager, text_converter)
    for page in PDFPage.get_pages(fp, pagenos=set(), maxpages=0, password="", caching=True, check_extractable=True):
        interpreter.process_page(page)
    text = out_text.getvalue()
    fp.close()
    text_converter.close()
    out_text.close()
    return text

def minepdffr(pdf):
    file1 = open('MineResultFrancais.txt', "w", encoding='utf-8')
    text = get_pdf_file_content(pdf)
    file1.write(text)

def convertpdf2image(path_to_pdf):
    images = convert_from_path(path_to_pdf)
    for i in range(1,len(images)):
        images[i].save("page"+str(i+1)+".jpg","JPEG")

def pdfPages(Pdf):
    file = open(Pdf,"rb")
    readpdf =PyPDF2.PdfFileReader(file)
    return readpdf.numPages

def deleteSommaireImages(pages):
    for i in range(2,pages+1):
        if os.path.exists("page"+str(i)+".jpg"):
            os.remove("page"+str(i)+".jpg")
        else: print("The file does not exist")

def deleteTextImages(start,pages):
    for i in range(start+1,pages):
        if os.path.exists("page"+str(i)+".jpg"):
            os.remove("page"+str(i)+".jpg")
        else: print("The file does not exist")

def coupeimages(start, pages):
    for i in range(start+1,pages+1):
        im = Image.open("page"+str(i)+".jpg")
        width, height = im.size
        x = width / 2
        y = 150
        im1 = im.crop((x, y, width, height))
        im1.save(str(i)+"RightPage.jpg", "JPEG")
        x = 0
        y = 150
        im1 = im.crop((x, y, width / 2, height))
        im1.save(str(i)+"LeftPage.jpg", "JPEG")
        os.remove("page"+str(i)+".jpg")

def ocrSommaire(pages):
    for i in range(2,pages+1):
        ocr("page"+str(i))
        os.remove("page" + str(i) + ".jpg")

def ocrText(sommaire,pages):
    for i in range(sommaire+1,pages+1):
        ocr(str(i)+"LeftPage")
        ocr(str(i) + "RightPage")
        os.remove(str(i) + "RightPage.jpg")
        os.remove(str(i) + "LeftPage.jpg")

def groupSommairefrancais(pages):
    filesommaire=open("sommairefrancais.txt","w",encoding="UTF-8")
    for i in range(2,pages+1):
        file=open("page"+str(i)+".txt","r")
        filesommaire.write(file.read())
        file.close()
        os.remove("page" + str(i) + ".txt")
    filesommaire.close()

def groupTextFrancais(sommaire,pages):
    fileText = open("totalfrancais.txt", "w",encoding="UTF-8")
    for i in range(sommaire+1,pages+1):
        fileText.write("\npage"+str(i)+"  \n")
        file = open(str(i) + "Leftpage.txt", "r",encoding="UTF-8")
        fileText.write(file.read())
        file.close()
        os.remove(str(i) + "Leftpage.txt")
        file = open(str(i) + "Rightpage.txt", "r",encoding="UTF-8")
        fileText.write(file.read())
        file.close()
        os.remove(str(i) + "Rightpage.txt")
    fileText.close()

def pagesfinder(start,finish):
    file = open("totalArabic.txt", 'r', encoding="UTF-8")
    cpt=start+1
    matches=[]
    text = file.read()
    text = text.replace("\n", " ")
    text = text.replace(" |", "")
    for i in range(start,finish+1):
        allmatches = re.finditer(pattern="page"+str(i), string=text)
        for match in allmatches:
                print(cpt)
                print(match)
                matches.append(match)
                cpt+=1
    return matches

def download_file(download_url, filename):
    response = urllib.request.urlopen(download_url)
    file = open(filename + ".pdf", 'wb')
    file.write(response.read())
    file.close()

def minepdf(pdf):
    file1 = open('MineResult.txt', "w", encoding='utf-8')
    text = get_pdf_file_content(pdf)
    file1.write(text)
    file1.close()

def getSommaireArab(file):
    file1 = open(file, "r", encoding='utf-8')
    count = 0
    lines = file1.readlines()
    pair = True
    for line in lines:
        if (re.search("فهرس", line)):
            print(line)
            page = lines[count - 2]
            page = page.replace("\n", "")
            page = page.replace("", "")
            if (pair):
                if(page.isnumeric()):
                    print("2 lines")
                    print(lines[count - 2])
                    last = int(page)
                    pair = False
                    print(f"page {page}")
                    print(f"last {last}")
            else:
                print("7 lines")
                page = lines[count - 7]
                page = page.replace("\n", "")
                page = page.replace("", "")
                print(page.isnumeric())
                if(page.isnumeric()):
                    last = int(page)
                    print(f"page {page}")
                    print(f"last {last}")
                    pair = True
        count = count + 1
    print(f"last {last}")
    file1.close()
    return last

def groupTextArabic(sommaire,pages):
    fileText = open("totalArabic.txt", "w", encoding="UTF-8")
    for i in range(sommaire+1,pages+1):
        fileText.write("\npage"+str(i)+"  \n")
        file = open(str(i) +"Rightpage.txt", "r", encoding="UTF-8")
        fileText.write(file.read())
        file.close()
        os.remove(str(i) +"Rightpage.txt")
        file = open(str(i) + "Leftpage.txt", "r", encoding="UTF-8")
        fileText.write(file.read())
        file.close()
        os.remove(str(i) + "Leftpage.txt")
    fileText.close()


def getText(num,annee):
    filenameFR=""
    filenameAR=""
    if (num > 0 and 10 > num):
        filenameAR=f"A{annee}00{num}.pdf"
        filenameFR=f"F{annee}00{num}.pdf"
        download_file(f"https://www.joradp.dz/FTP/jo-arabe/{annee}/A{annee}00{num}.pdf",f"A{annee}00{num}")
        download_file(f"https://www.joradp.dz/FTP/jo-francais/{annee}/F{annee}00{num}.pdf", f"F{annee}00{num}")
    elif (num > 9 and 100 > num):
        filenameAR = f"A{annee}0{num}.pdf"
        filenameFR = f"F{annee}0{num}.pdf"
        download_file(f"https://www.joradp.dz/FTP/jo-arabe/{annee}/A{annee}0{num}.pdf", f"A{annee}0{num}")
        download_file(f"https://www.joradp.dz/FTP/jo-francais/{annee}/F{annee}0{num}.pdf", f"F{annee}0{num}")
    else:
        filenameAR = f"A{annee}{num}.pdf"
        filenameFR = f"F{annee}{num}.pdf"
        download_file(f"https://www.joradp.dz/FTP/jo-arabe/{annee}/A{annee}{num}.pdf", f"A{annee}{num}")
        download_file(f"https://www.joradp.dz/FTP/jo-francais/{annee}/F{annee}{num}.pdf", f"F{annee}{num}")
    pages = pdfPages(filenameAR)
    convertpdf2image(filenameAR)
    coupeimages(2, pages)
    ocrText(2, pages)
    groupTextArabic(2, pages)
    pages = pdfPages(filenameFR)
    convertpdf2image(filenameFR)
    coupeimages(2, pages)
    ocrText(2, pages)
    groupTextFrancais(2,pages)

def preparetext(text):
    result=text.replace("\n", " ")
    result=result.replace(" |", " ")
    return result

def gettextes(Results):
    fileFR=open("totalfrancais.txt",'r',encoding="UTF-8")
    fileAR=open("totalArabic.txt",'r',encoding="UTF-8")
    Orderfr=[]
    OrderAr=[]
    francais=fileFR.read()
    francaisprepared=preparetext(francais)
    arabe=fileAR.read()
    arabeprepared=preparetext(arabe)
    print(francaisprepared)
    print(f"size of result:{len(Results)}")
    fileAR.close()
    fileFR.close()
    i = 0
    for r in Results:
        matches=[]
        allmatches = re.finditer(r.rechercheAR,arabeprepared,flags=re.IGNORECASE)
        for m in allmatches:
            matches.append(m)
        if(len(matches)==1):
            for m in matches:
                OrderAr.append(m.end())
        elif (len(matches) == 2):
            print(f"text 2: {r.rechercheAR}")
            OrderAr.append(matches[0].end())
        elif (len(matches)==0):
            print("0000")
            print(r.rechercheAR[:-25])
            allmatches = re.finditer(r.rechercheAR[30:], arabeprepared, flags=re.IGNORECASE)
            for m in allmatches:
                matches.append(m)
            if (len(matches) == 1):
                for m in matches:
                    print("added ar1")
                    OrderAr.append(m.end())
            elif (len(matches) == 2):
                print(f"text 2: {r.rechercheAR}")
                OrderAr.append(matches[0].end())
            else:
                print(f"index : {Results.index(r)}")
                print(f"page ar {r.page_ar} {r.rechercheAR}")
                print("lookingpage"+str(r.page_ar))
                allmatches = re.finditer("page"+str(r.page_ar)+" ", arabeprepared, flags=re.IGNORECASE)
                for m in allmatches:
                    print("added ar2")
                    OrderAr.append(m.end())
                r.error = True
        else:
            print(f"index : {Results.index(r)}")
            print(f"page ar {r.page_ar} {r.rechercheAR}")
            print("lookingpage" + str(r.page_ar))
            allmatches = re.finditer("page" + str(r.page_ar) + " ", arabeprepared, flags=re.IGNORECASE)
            for m in allmatches:
                print("added ar2")
                OrderAr.append(m.end())
            r.error = True
        matches = []
        print(r.rechercheFR)
        allmatches = re.finditer(re.escape(r.rechercheFR), francaisprepared, flags=re.IGNORECASE)
        for m in allmatches:
            matches.append(m)
        if (len(matches) == 1):
            for m in matches:
                Orderfr.append(m.end())
        elif (len(matches) == 2):
            print(f"text 2: {r.rechercheFR}")
            print(matches[0].end())
            Orderfr.append(matches[0].end())
        elif (len(matches) == 0):
            print("0000")
            print("this line")
            print(r.rechercheFR[:-25])
            allmatches = re.finditer(re.escape(r.rechercheFR[:-25]), francaisprepared, flags=re.IGNORECASE)
            for m in allmatches:
                print("added")
                matches.append(m)
            if (len(matches) == 1):
                for m in matches:
                    Orderfr.append(m.end())
            elif (len(matches) == 2):
                print(f"text 2: {r.rechercheFR}")
                print(matches[0].end())
                Orderfr.append(matches[0].end())
            else:
                print("page fr")
                allmatches = re.finditer("page" + str(r.page_fr)+" ", francaisprepared, flags=re.IGNORECASE)
                for m in allmatches:
                    print("added page")
                    Orderfr.append(m.end())
                r.error = True
        else:
            print("page fr")
            allmatches = re.finditer("page" + str(r.page_fr) + " ", francaisprepared, flags=re.IGNORECASE)
            for m in allmatches:
                print("added page")
                Orderfr.append(m.end())
            r.error = True
    OrderAr=repareOrder(OrderAr)
    Orderfr=repareOrder(Orderfr)
    print(f"size of results:{len(Results)}")
    print(f"size of order:{len(Orderfr)} {len(OrderAr)}")
    print(OrderAr)
    print(Orderfr)
    for i in range(len(OrderAr)-1):
        Results[i].text_ar=arabeprepared[OrderAr[i]:OrderAr[i+1]]
    Results[len(OrderAr)-1].text_ar=arabeprepared[OrderAr[len(OrderAr)-1]:]
    for i in range(len(Orderfr)-1):
        Results[i].text_fr=francaisprepared[Orderfr[i]:Orderfr[i+1]]
    Results[len(Orderfr)-1].text_fr=francaisprepared[Orderfr[len(Orderfr)-1]:]
    return Results




def repareOrder(tab):
    i=0
    repared=[]
    repared.append(tab[0])
    for t in tab:
        if(i!=0):
            if(t>repared[i-1]):
                repared.append(t)
            else:
                repared.append(repared[i-1]+300)
        i+=1
    return repared

def DateFormat(date):
    return str(dateparser.parse(date).date())

def SecteurArabe(Minist):
    match Minist:
        case "وزارة الشؤون الخارجية والجالية الوطنية بالخارج":
            return "الشؤون الخارجية"
        case "وزارة الشؤون الدينية والأوقاف":
            return "الشؤون الدينية"
        case "وزارة الفلاحة والتنمية الريفية":
            return "الفلاحة"
        case "وزارة التجارة وترقية الصادرات":
            return "التجارة"
        case "وزارة الاتصال":
            return "الإتصال"
        case "وزارة الثقافة و الفنون":
            return "الثقافة"
        case "وزارة الدفاع الوطني":
            return "الدفاع الوطني"
        case "وزارة اقتصاد المعرفة والمؤسسات الناشئة":
            return "الإقتصاد"
        case "وزارة التربية الوطنية":
            return "التربية والتعليم العالي"
        case "وزارة الانتقال الطاقوي والطاقات المتجددة":
            return "الطاقة"
        case "وزارة البيئة":
            return "البيئة"
        case "وزارة المالية":
            return "المالية"
        case "وزارة التكوين والتعليم المهنيين":
            return "السكن"
        case "وزارة السكن والعمران والمدينة":
            return "الري"
        case "وزارة الصناعة":
            return "الصناعة"
        case "وزارة الداخلية والجماعات المحلية والتهيئة العمرانية":
            return "الداخلية والجماعات المحلية"
        case "وزارة الشباب والرياضة":
            return "الشباب والرياضة"
        case "وزارة العدل حافظ الأختام":
            return "العدل"
        case "وزارة الطاقة والمناجم":
            return "المناجم"
        case "وزارة المجاهدين وذوي الحقوق":
            return "المجاهدين"
        case "وزارة العلاقات مع البرلمان":
            return "البرلمان"
        case "وزارة الصيد البحري والمنتجات الصيدية":
            return "الصيد"
        case "وزارة البريد والمواصلات السلكية واللاسلكية":
            return "البريد"
        case "وزارة الرقمنة و الاحصائيات":
            return "نظرة استشرافية وإحصائيات"
        case "وزارة التربية الوطنية":
            return "البحث العلمي"
        case "وزارة الصحة":
            return "الصحة"
        case "وزارة التضامن الوطني والأسرة وقضايا المرأة":
            return "التضامن"
        case "وزارة السياحة والصناعة التقليدية":
            return "السياحة"
        case "وزارة النقل":
            return "النقل"
        case "وزارة العمل والتشغيل والضمان الاجتماعي":
            return "العمل"
        case "وزارة الأشغال العمومية":
            return "الأشغال العمومية"
        case "وزارة المؤسسات المصغرة":
            return "الإقتصاد"
        case "وزارة التعليم العالي و البحث العلمي":
            return "التربية والتعليم العالي"
        case "وزارة الصناعة الصيدلانية":
            return "الصناعة"
        case _:
            return ""


def SecteurFrancais(Minist):
    match Minist:
        case "وزارة الشؤون الخارجية والجالية الوطنية بالخارج":
            return "AFFAIRES ETRANGERES"
        case "وزارة الشؤون الدينية والأوقاف":
            return "AFFAIRES RELIGIEUSES"
        case "وزارة الفلاحة والتنمية الريفية":
            return "AGRICULTURE"
        case "وزارة التجارة وترقية الصادرات":
            return "COMMERCE"
        case "وزارة الاتصال":
            return "COMMUNICATION"
        case "وزارة الثقافة و الفنون":
            return "CULTURE"
        case "وزارة الدفاع الوطني":
            return "DEFENSE NATIONALE"
        case "وزارة اقتصاد المعرفة والمؤسسات الناشئة":
            return "ECONOMIE"
        case "وزارة التربية الوطنية":
            return "EDUCATION ET ENSEIGNEMENT SUPERIEUR"
        case "وزارة الانتقال الطاقوي والطاقات المتجددة":
            return "ENERGIE"
        case "وزارة البيئة":
            return "ENVIRONNEMENT"
        case "وزارة المالية":
            return "FINANCES"
        case "وزارة التكوين والتعليم المهنيين":
            return "HABITAT"
        case "وزارة الموارد المائية والأمن المائي":
            return "HYDRAULIQUE ET EAU"
        case "وزارة الصناعة":
            return "INDUSTRIES"
        case "وزارة الداخلية والجماعات المحلية والتهيئة العمرانية":
            return "INTERIEUR ET COLLECTIVITES LOCALES"
        case "وزارة الشباب والرياضة":
            return "JEUNESSE ET SPORT"
        case "وزارة العدل حافظ الأختام":
            return "JUSTICE"
        case "وزارة الطاقة والمناجم":
            return "MINES"
        case "وزارة المجاهدين وذوي الحقوق":
            return "MOUDJAHIDINE"
        case "وزارة العلاقات مع البرلمان":
            return "PARLEMENT"
        case "وزارة الصيد البحري والمنتجات الصيدية":
            return "PECHE"
        case "وزارة البريد والمواصلات السلكية واللاسلكية":
            return "POSTES ET TELECOMMUNICATIONS"
        case "وزارة الرقمنة و الاحصائيات":
            return "PROSPECTIVE ET STATISTIQUE"
        case "وزارة التعليم العالي و البحث العلمي":
            return "RECHERCHE SCIENTIFIQUE"
        case "وزارة الصحة":
            return "SANTE"
        case "وزارة التضامن الوطني والأسرة وقضايا المرأة":
            return "SOLIDARITE"
        case "وزارة السياحة والصناعة التقليدية":
            return "TOURISME ET ARTISANAT"
        case "وزارة النقل":
            return "TRANSPORT"
        case "وزارة العمل والتشغيل والضمان الاجتماعي":
            return "TRAVAIL"
        case "وزارة الأشغال العمومية":
            return "TRAVAUX PUBLICS"
        case "وزارة المؤسسات المصغرة":
            return "ECONOMIE"
        case "وزارة التعليم العالي و البحث العلمي":
            return "EDUCATION ET ENSEIGNEMENT SUPERIEUR"
        case "وزارة الصناعة الصيدلانية":
            return "INDUSTRIES"
        case _:
            return ""

def finalisation(Results):
    temp=[]
    for r in Results:
        temp.append(Result(r.file_name_ar,r.ministry_ar,r.title_ar,r.page_ar,r.type_text_ar,r.text_ar,SecteurArabe(r.ministry_ar),r.keywords_ar,r.file_name_fr,r.ministry_fr,r.title_fr,r.page_fr,r.type_text_fr,r.text_fr,SecteurFrancais(r.ministry_ar),r.keywords_fr,DateFormat(r.date).replace("-", ""),r.year,r.error))
    return temp

class sequence:
    def __init__(self,year,seq):
        self.year=year
        self.seq=seq

class users:
    def __init__(self,prenom,email,secteur):
        self.prenom=prenom
        self.email=email
        self.secteur=secteur

def getsequence():
    SUPERBASE_HEADERS: str = {
        'apikey': "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVzemh3d3JtaXVjdGlncHFidnh2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE2NTY0MzYzMTUsImV4cCI6MTk3MjAxMjMxNX0.d9Unw7tN4qsuTZ4mjuQkkWS3awjYUmSr7Z0t_X_2VU4",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVzemh3d3JtaXVjdGlncHFidnh2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE2NTY0MzYzMTUsImV4cCI6MTk3MjAxMjMxNX0.d9Unw7tN4qsuTZ4mjuQkkWS3awjYUmSr7Z0t_X_2VU4"}
    SUPERBASE_URL: str = 'https://uszhwwrmiuctigpqbvxv.supabase.co'
    SUPERBASE_KEY: str = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVzemh3d3JtaXVjdGlncHFidnh2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE2NTY0MzYzMTUsImV4cCI6MTk3MjAxMjMxNX0.d9Unw7tN4qsuTZ4mjuQkkWS3awjYUmSr7Z0t_X_2VU4'
    supabase: Client = create_client(SUPERBASE_URL, SUPERBASE_KEY)
    data = data = supabase.table("Identifient").select("*").execute()
    seq = data.data[0]['seq']
    year =data.data[0]['year']
    return sequence(year,seq)

def getid():
    SUPERBASE_HEADERS: str = {
        'apikey': "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVzemh3d3JtaXVjdGlncHFidnh2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE2NTY0MzYzMTUsImV4cCI6MTk3MjAxMjMxNX0.d9Unw7tN4qsuTZ4mjuQkkWS3awjYUmSr7Z0t_X_2VU4",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVzemh3d3JtaXVjdGlncHFidnh2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE2NTY0MzYzMTUsImV4cCI6MTk3MjAxMjMxNX0.d9Unw7tN4qsuTZ4mjuQkkWS3awjYUmSr7Z0t_X_2VU4"}
    SUPERBASE_URL: str = 'https://uszhwwrmiuctigpqbvxv.supabase.co'
    SUPERBASE_KEY: str = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVzemh3d3JtaXVjdGlncHFidnh2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE2NTY0MzYzMTUsImV4cCI6MTk3MjAxMjMxNX0.d9Unw7tN4qsuTZ4mjuQkkWS3awjYUmSr7Z0t_X_2VU4'
    supabase: Client = create_client(SUPERBASE_URL, SUPERBASE_KEY)
    data = data = supabase.table("Sequence").select("*").execute()
    return data.data[0]['seq']

def setid(seq):
    SUPERBASE_HEADERS: str = {
        'apikey': "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVzemh3d3JtaXVjdGlncHFidnh2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE2NTY0MzYzMTUsImV4cCI6MTk3MjAxMjMxNX0.d9Unw7tN4qsuTZ4mjuQkkWS3awjYUmSr7Z0t_X_2VU4",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVzemh3d3JtaXVjdGlncHFidnh2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE2NTY0MzYzMTUsImV4cCI6MTk3MjAxMjMxNX0.d9Unw7tN4qsuTZ4mjuQkkWS3awjYUmSr7Z0t_X_2VU4"}
    SUPERBASE_URL: str = 'https://uszhwwrmiuctigpqbvxv.supabase.co'
    SUPERBASE_KEY: str = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVzemh3d3JtaXVjdGlncHFidnh2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE2NTY0MzYzMTUsImV4cCI6MTk3MjAxMjMxNX0.d9Unw7tN4qsuTZ4mjuQkkWS3awjYUmSr7Z0t_X_2VU4'
    supabase: Client = create_client(SUPERBASE_URL, SUPERBASE_KEY)
    data = supabase.table("Sequence").update({"seq": seq}).eq("id", 1).execute()

def increment(seq):
    SUPERBASE_HEADERS: str = {'apikey': "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVzemh3d3JtaXVjdGlncHFidnh2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE2NTY0MzYzMTUsImV4cCI6MTk3MjAxMjMxNX0.d9Unw7tN4qsuTZ4mjuQkkWS3awjYUmSr7Z0t_X_2VU4","Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVzemh3d3JtaXVjdGlncHFidnh2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE2NTY0MzYzMTUsImV4cCI6MTk3MjAxMjMxNX0.d9Unw7tN4qsuTZ4mjuQkkWS3awjYUmSr7Z0t_X_2VU4"}
    SUPERBASE_URL: str = 'https://uszhwwrmiuctigpqbvxv.supabase.co'
    SUPERBASE_KEY:str ='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVzemh3d3JtaXVjdGlncHFidnh2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE2NTY0MzYzMTUsImV4cCI6MTk3MjAxMjMxNX0.d9Unw7tN4qsuTZ4mjuQkkWS3awjYUmSr7Z0t_X_2VU4'
    supabase: Client = create_client(SUPERBASE_URL, SUPERBASE_KEY)
    seq+=1
    data = supabase.table("Identifient").update({"seq":seq}).eq("id", 1).execute()


def verifyYear(seq):
    current_year = date.today().year
    if(seq.year!=current_year):
        return sequence(seq.year+1,1)
    else:
        return seq



def injectdataVSC(json):
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        # Handle target environment that doesn't support HTTPS verification
        ssl._create_default_https_context = _create_unverified_https_context

    app_search = AppSearch(
        "https://vps.juriste-dz.com/",  # Endpoint
        http_auth="private-tr1mjxvtsg5e66dntc2x6pb3",
        # Private key, grants read/write access only to the engine "journal-officiel-veille"
        ca_certs=False,
        verify_certs=False,
    )
    engine_name = "journal-officiel-veille"
    # If the following runs, then connection is established
    app_search.get_schema(engine_name)

    response = app_search.index_documents(
        engine_name=engine_name,
        body=json,request_timeout=30
    )

def getUsers():
    listusers=[]
    SUPERBASE_HEADERS: str = {
        'apikey': "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVzemh3d3JtaXVjdGlncHFidnh2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE2NTY0MzYzMTUsImV4cCI6MTk3MjAxMjMxNX0.d9Unw7tN4qsuTZ4mjuQkkWS3awjYUmSr7Z0t_X_2VU4",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVzemh3d3JtaXVjdGlncHFidnh2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE2NTY0MzYzMTUsImV4cCI6MTk3MjAxMjMxNX0.d9Unw7tN4qsuTZ4mjuQkkWS3awjYUmSr7Z0t_X_2VU4"}
    SUPERBASE_URL: str = 'https://uszhwwrmiuctigpqbvxv.supabase.co'
    SUPERBASE_KEY: str = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVzemh3d3JtaXVjdGlncHFidnh2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE2NTY0MzYzMTUsImV4cCI6MTk3MjAxMjMxNX0.d9Unw7tN4qsuTZ4mjuQkkWS3awjYUmSr7Z0t_X_2VU4'
    supabase: Client = create_client(SUPERBASE_URL, SUPERBASE_KEY)
    data = data = supabase.table("users").select("*").execute()
    for d in data.data:
        listusers.append(users(d['Prenom'],d['email'],d['secteur']))
    return listusers

def getSecteur(Final,secteur):
    return [x for x in Final if x.sectors_fr == secteur]

def generateHTML(objects):
    html=""

    for obj in objects:
        pprint(vars(obj))
        type=obj.type_text_fr.replace(" ", "-")
        html+=f"<h3>{obj.ministry_fr}</h3><p>{obj.title_fr}</p><a href=\"https://veille.juriste-dz.com/fr/journal-officiel/{obj.id}/{type}/\">Lire La suite</a>"
    return html

def sendEmail(user,objects):
    EMAIL_ADDRESS = 'veille.juriste.dz@gmail.com'
    EMAIL_PASSWORD = 'ucncmqjepyimsrqj'
    msg = EmailMessage()
    msg['Subject'] = 'Votre veille juridique'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = user.email
    titles=generateHTML(objects)
    print()
    print(f"titles {titles}")
    message=f'''
    <!DOCTYPE html>
        <html>
            <body>
                <div style="background-color:#eee;padding:10px 20px; text-align: center" >
                <img src="https://juriste-dz.com/static/media/logo.dfed61fc.png" style="height: 150px;">
                    <h2 style="font-family:Georgia, 'Times New Roman', Times, serif;color#454349;">Votre Veille Juridique</h2>
                </div>
                <div style="text-align:center">
                    <div >
                        
                        <div style="text-align:center;">
                            {titles}
                            
                        </div>
                    </div>
                </div>
            </body>
        </html>
    '''
    msg.set_content(message, subtype='html')

    server= smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    if(titles!=None):
        server.send_message(msg)


def sendNotification(email):
    EMAIL_ADDRESS = 'veille.juriste.dz@gmail.com'
    EMAIL_PASSWORD = 'ucncmqjepyimsrqj'
    msg = EmailMessage()
    msg['Subject'] = 'Nouveaux textes'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = email
    print(f"titles ")
    msg.set_content(f'''
    <!DOCTYPE html>
        <html>
            <body>
                <div style="background-color:#eee;padding:10px 20px; text-align: center" >
                <img src="https://juriste-dz.com/static/media/logo.dfed61fc.png" style="height: 150px;">
                    
                </div>
                <div style="text-align:center">
                    <div >

                        <div style="text-align:center;">
                            <h1 style="font-family:Georgia, 'Times New Roman', Times, serif;color#454349;">De nouveaux textes sont injectés</h1>

                        </div>
                    </div>
                </div>
            </body>
        </html>
    ''', subtype='html')

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    server.send_message(msg)


def increment(seq):
    SUPERBASE_HEADERS: str = {'apikey': "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVzemh3d3JtaXVjdGlncHFidnh2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE2NTY0MzYzMTUsImV4cCI6MTk3MjAxMjMxNX0.d9Unw7tN4qsuTZ4mjuQkkWS3awjYUmSr7Z0t_X_2VU4","Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVzemh3d3JtaXVjdGlncHFidnh2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE2NTY0MzYzMTUsImV4cCI6MTk3MjAxMjMxNX0.d9Unw7tN4qsuTZ4mjuQkkWS3awjYUmSr7Z0t_X_2VU4"}
    SUPERBASE_URL: str = 'https://uszhwwrmiuctigpqbvxv.supabase.co'
    SUPERBASE_KEY:str ='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVzemh3d3JtaXVjdGlncHFidnh2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE2NTY0MzYzMTUsImV4cCI6MTk3MjAxMjMxNX0.d9Unw7tN4qsuTZ4mjuQkkWS3awjYUmSr7Z0t_X_2VU4'
    supabase: Client = create_client(SUPERBASE_URL, SUPERBASE_KEY)
    data = supabase.table("Identifient").update({"seq":seq+1}).eq("id", 1).execute()

def affectseq(list):
    seq=getid()
    for l in list:
        l.id=seq
        seq+=1
    setid(seq)
    return list

def DoWork():
    '''seq=verifyYear(getsequence())'''
    num=50
    annee=2022
    getText(num,annee)
    result=traitement(num,annee)
    Final=gettextes(result)
    Final=finalisation(Final)
    listofusers=getUsers()
    Final=affectseq(Final)
    for u in listofusers:
        print(f"secteur {u.secteur}")
        sect=getSecteur(Final, u.secteur)
        if(len(sect)!=0):
            sect = getSecteur(Final, u.secteur)
        sendEmail(u,sect)
    file=open(f"{annee}{num}.json","w",encoding="UTF-8")
    json_str = json.dumps([ob.__dict__ for ob in Final])
    file.write(json_str)
    file.close()
    injectdataVSC(json_str)
    sendNotification("dridanas@gmail.com")
    sendNotification("ga_drid@esi.dz")
    increment(num)

