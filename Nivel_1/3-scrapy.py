#El mismo ejercicio del problema 2 pero con Scrapy

from scrapy.item import Field,Item
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.loader import ItemLoader

#Primero tengo que definir las propiedades que tendrá mis items en una clase, hereda de Item object
#Vamos a modelarla según los datos que extraigamos
class Pregunta(Item):
    id = Field()
    titulo = Field()
    descripcion = Field()

#Esta clase es como la función main de Scrapy, aquí sucede todo el proceso
class StackOverflowSpider(Spider):
    #Nota: los nombres de las variablesy funciones como start_url y parse tienen que llamarse así, de lo contrario no funcionará
    name = "mi_primer_spider"

    #Así se definen los headers en scrapy
    custom_settings = {
        'USER_AGENT' : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36" 
    }

    #Url semillas, Scrapy hace las peticiones de manera automática, no necesitamos utilizar otra librería como requests
    start_urls = ['https://stackoverflow.com/questions/']

    #Con esta función hace 
    def parse(self,response):
        #El objeto Selector es cómo el objeto HTML o Soup con el cuál podemos navegar sobre el HTML
        sel = Selector(response)
        #Podemos utilizar expresiones xpath
        preguntas = sel.xpath('//div[@id="questions"]//div[contains(@id,"question-summary")]')
        i = 0
        for pregunta in preguntas:
            #Instanciamos un objeto del Item pregunta, y le pasamos el div del contenedor de la pregunta y la descripción
            #Al pasarle el div, las busquedas relativas que hagamos se harán desde este div
            item = ItemLoader(Pregunta(),pregunta)
            item.add_xpath('titulo','.//div[@class="s-post-summary--content"]/h3/a/text()')
            item.add_xpath('descripcion','.//div[@class="s-post-summary--content-excerpt"]/text()')
            item.add_value('id',i)
            i+=1

            yield item.load_item()
