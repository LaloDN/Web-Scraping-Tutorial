#Extraer datos de noticias de la página de El Universo en la sección de deportes con Scrapy y BeautifulSoup
from scrapy.item import Field,Item
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from bs4 import BeautifulSoup
from bs4.element import Tag

class Noticia(Item):
    id = Field()
    titulo = Field()
    preview = Field()

    
class ElUniversalDeportes(Spider):
    name = "spider_noticias"

    custom_settings = {
        'USER_AGENT' : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36" 
    }

    start_urls = ['https://www.eluniverso.com/deportes/']

    """def parse(self,response):
        sel = Selector(response)
        i = 0
        contenedores = sel.xpath('(//ul[contains(@class,"feed")])[2]/li')
        for contenedor in contenedores:
            item = ItemLoader(Noticia(),contenedor)
            item.add_value('id',i)
            item.add_xpath('titulo','.//h2/a/text()')
            item.add_xpath('preview','.//p/text()')
            i+=1

            yield item.load_item()
    """

    #Ejemplo con beautifulsoup en lugar del selector de scrapy
    def parse(self,response):
        soup = BeautifulSoup(response.body)
        i = 0
        contenedores = soup.find_all('ul',class_='feed')[1]
        for contenedor in contenedores:
            item = ItemLoader(Noticia(), response.body)
            #EL parámetro recursive es el equivalente a los dos slash de xpath // para buscar en cualquiera de los hijos del elemento
            titular = contenedor.find('h2',recursive=True).find('a').text
            preview = contenedor.find('p',recursive=True).text
            item.add_value('id',i)
            item.add_value('titulo',titular)
            item.add_value('preview',preview)

            i+=1
            yield item.load_item()