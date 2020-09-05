import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl
import webbrowser
import re

def pegar_html(url):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    html = urllib.request.urlopen(url, context=ctx).read()
    soup = BeautifulSoup(html, 'html.parser')
    return soup



def pegar_canais_espn(soup):
    a = soup.findAll("section")
    dicionario = {}
    for item in a:
        if item.get("class",None)==['Carousel', 'relative', 'Carousel--dark', 'Carousel--watch', 'Carousel--16x9', 'Carousel--hasMeta']:
            if (item.find(id="bucket-392"))!=None:
                lis = item.findAll("li")
                for i,li in enumerate(lis):
                    divs = li.findAll("div")
                    for div in divs:
                        if div.get("class",None)==['WatchTile__Content']:
                            ultima = div.findAll("div")
                            for coisa in ultima:
                                if coisa.get("class",None)==["WatchTile__Meta"]:
                                    for lugar_link in (li.findAll("a")):
                                        dicionario[coisa.get_text()] = lugar_link.get("href",None)
    
    return dicionario

def checar_canais_espn(dicionario):
    for programa,link in dicionario.items():
        nba = re.findall(".*NBA.*",programa)
        if len(nba)>0:
            webbrowser.open('https://www.espn.com.br' + link)
            return True
    return False

def ir_para_globosat(tem_na_espn):
    if tem_na_espn == False:
        webbrowser.open('https://globosatplay.globo.com/')

def main():
    html_que_importa = pegar_html('https://www.espn.com.br/watch/?country=br&lang=pt&redirected=true')
    dicionario_canais_espn = pegar_canais_espn(html_que_importa)
    tem_na_espn = checar_canais_espn(dicionario_canais_espn)
    ir_para_globosat(tem_na_espn)
main()