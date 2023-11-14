import requests 
from lxml import html

url = 'https://www.eluniverso.com/deportes/'
headers = {
    #Sobreescribimos el user-agent por default
    "user-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36" 
}

respuesta = requests.get(url,headers=headers)

parser : html.HtmlElement = html.fromstring(respuesta.text)

expresion = '//ul[contains(@class,"feed")]//li//h2/a/text()'
expresion2 = '//ul[contains(@class,"feed")]//li//p/text()'
lis = parser.xpath(expresion2)
for li in lis:
    print(li)