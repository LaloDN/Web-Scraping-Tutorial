#Extrae los datos de la selección de nombres de la página de Wikipedia
import requests
from lxml import html

#Definimos la URL para hacer el requerimento
url = "https://www.wikipedia.org/"
#Headers para el request
headers = {
    #Sobreescribimos el user-agent por default
    "user-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36" 
}

respuesta = requests.get(url,headers=headers)
 #El request nos trae una respuesta html en formato string, con la librería lxml lo parseamos a un objeto HTML puro para trabjar con el
parser : html.HtmlElement = html.fromstring(respuesta.text)

#Buscamos un elemento por herramientas del parser y accedemos a su contenido
#etiqueta_ingles = parser.get_element_by_id('js-link-box-en')
#print(etiqueta_ingles.text_content())

#Buscamos un elemento por xpath
#expresion = "//a[@id='js-link-box-en']/strong/text()"
#etiqueta_ingles = parser.xpath(expresion)
#print(etiqueta_ingles)

#Obtener todas las etiquetas
expresion = "/html/body/div[@class='central-featured']/div/a/strong/text()" #Esta es una solución válida 
expresion2 = "//div[contains(@class,'central-featured-lang')]//strong/text()" #Otra posible solución
etiquetas = parser.xpath(expresion2)
for idioma in etiquetas:
    print(idioma)

idiomas = parser.find_class('central-featured-lang')
for idioma in idiomas:
    print(idioma.text_content())