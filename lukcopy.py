import sys
import urllib.request as urlRequest
import urllib.parse as urlParse
import os
import errno
import io
from bs4 import BeautifulSoup
import string

url = ""
folder_output = "template_luk"

def usage():
    print("Luk Copy")
    print(" ")
    print("Usage: lukcopy.py -url target_host -o output")
    print(" ")
    print("Examples: ")
    print("lukcopy.py -url https://ndon.pl/themes/ZUPA/1.01/index.html -o /var/www/py/template")
    sys.exit(0)

def main():
    global url
    global folder_output
    if not len(sys.argv[1:]):
        usage()
    print("Processando...")

    if not len(sys.argv[2]):
        usage()
    url = sys.argv[2]


    if not len(sys.argv[4]):
        folder_output = 'template_luk'
    else:
        folder_output = sys.argv[4]

    importPages()

def importPages():
    global url
    values = {}
    headers = {
        "User-Agent": "Mozilla/5.0 ( X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36",
        "Upgrade-Insecure-Requests": 1}
    values = urlParse.urlencode(values)
    values = values.encode("UTF-8")
    targetUrl = urlRequest.Request(url=url, data=values, headers=headers)
    x = urlRequest.urlopen(targetUrl)
    sourceCode = x.read()
    importIndex(sourceCode)
    importImg(sourceCode)
    importCss(sourceCode)
    importJS(sourceCode)

def importIndex(index):
    global folder_output
    print("importing index...")
    try:
        os.makedirs(folder_output)
        with io.FileIO(folder_output + "/index.html", "w") as file:
            file.write(index)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(folder_output):
            print('Pasta ja existe')
        else:
            print('Erro ao criar pasta')

    print("import index.html")
    print("---------------")

def importImg(index):
    print('---------------- import images ------------------')
    global url
    bsObj = BeautifulSoup(index, "lxml")
    results = bsObj.findAll("img")
    for result in results:
        try:
            urlImg = result.get("src")
            if(urlImg is not None):
                srcImg = urlImg.split('/')
                createFolderOrFile(srcImg)
        except:
            print("not import----------->"+urlImg)

def importCss(index):
    print('---------------- import css ------------------')
    global url
    bsObj = BeautifulSoup(index, "lxml")
    results = bsObj.findAll("link")
    for result in results:
        try:
            urlCss = result.get("href")
            if(urlCss is not None):
                srcCss = urlCss.split('/')
                createFolderOrFile(srcCss)
        except:
            print("not import----------->"+urlCss)

def importJS(index):
    print('---------------- import js ------------------')
    global url
    bsObj = BeautifulSoup(index, "lxml")
    results = bsObj.findAll("script")
    for result in results:
        try:
            urlJs = result.get("src")
            if(urlJs is not None):
                print(urlJs)
                srcJs = urlJs.split('/')
                createFolderOrFile(srcJs)
        except:
            print("not import----------->"+urlJs)

def createFolderOrFile(srcUrl):
    global folder_output
    global url
    folder_pass = folder_output
    folder_clear = ''
    if srcUrl:
        for result in srcUrl:
            if (result.find('http')==-1):
                if (result.find('.')==-1):
                    folder_pass += '/'+result
                    folder_clear += '/'+result
                else:
                    img = folder_clear +'/'+ result
                    urlClear = clearUrl(url)
                    urlClear += img
                    index = getContent(urlClear)
                    try:
                        os.makedirs(folder_pass)
                    except OSError as exc:
                        if exc.errno == errno.EEXIST and os.path.isdir(folder_output):
                            print('Pasta ja existe')
                        else:
                            print('Erro ao criar pasta')
                    with io.FileIO(folder_pass +'/'+  result, "w") as file:
                        file.write(index)

def getContent(url):
    values = {"q": "python urllib"}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"}
    values = urlParse.urlencode(values)
    values = values.encode("UTF-8")
    targetUrl = urlRequest.Request(url=url, data=values, headers=headers)
    x = urlRequest.urlopen(targetUrl)
    if (x):
        return x.read()
    else:
        return null
    

def clearUrl(url):
    urlResult = ''
    if (url.find('.html') != -1):
        varurl = url.split('/')
        for list in varurl:
            if (list.find('.html') == -1):
                urlResult += list+'/'
    return urlResult

main()





