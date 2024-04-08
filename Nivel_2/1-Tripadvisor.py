#Extracción de datos de tripadvisor
from scrapy.item import Field,Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor

#Esta es la clase del item de los datos que vamos a extraer
class Hotel(Item):
    nombre = Field()
    precio = Field()
    descripcion = Field()
    amenities = Field()

#Cómo ya no es una sola página estática, ya no hereda de Spider, hereda de CrawlSpider para 
#extracción vertical u horizontal
class TripAdvisor(CrawlSpider):
    name = "Hotel_scraper"
    custom_settings = {
        'USER_AGENT' : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36" 
    }
    start_urls = ['https://www.tripadvisor.com/Hotels-g303845-Guayaquil_Guayas_Province-Hotels.html']

    #Esperamos un tiempo entre requerimentos para que no nos baneen
    download_delay = 2

    #Aquí definimos los links a los cuales podemos movernos, las reglas tenemos que sacarlas nosotros,
    #hay que ver que patrón siguen las URL de los items a investigar
    rules = (
        Rule(
            #Lo que hace el LinkExtractor es: desde la url semilla, en la respuesta, busca todos los links que haya dentro
            #del HTML, y dentro de cada LINK que encuentre, busca todos aquellos que tengan en cualquier lado el patrón
            #que definimos en la función, es cómo el comando LIKE "%something%" de SQL
            LinkExtractor(
                allow = r'/Hotel_Review-' 
            ), 
            follow = True, #Podemos definir si los links que pusimos los sigamos o no
            callback = "parse_hotel" #Función a la que se mandará a llamar cada que hagamos un request 
        ),
    )

    #Esta es una función que se le pasa al MapCompose para limpiar un dato durante el procesamiento
    #En este ejemplo se recibe una lista de precios, pero no es necesario tratar el parámetro texto como 
    #una lista de variables, si no como un string normal, Scrapy mapeará esta función con cada objeto
    def limpiar_precio(self,texto):
        new_price = texto.replace('MX$','').replace(',','')
        return int(new_price)

    def parse_hotel(self,response):
        sel = Selector(response)
        item = ItemLoader(Hotel(),sel)

        item.add_xpath('nombre','//h1[@id="HEADING"]/text()')
        item.add_xpath('precio',
                    '//div[@id="DEALS"]/div[position() = (last()-1)]/div/a/div[3]/div[position() =last()]/div/text()',
                    MapCompose(self.limpiar_precio))
        #item.add_xpath('descripcion','(//div[contains(@class,"ui_column")])[15]/div[3]/div/div/text()')
        item.add_xpath('descripcion','(//div[contains(@class,"ui_column")])[15]/div[position() = (last()-2)]/div/div/text()')
        item.add_xpath('amenities','(//div[contains(@class,"ui_column")])[16]/div[1]/div[2]/div/text()')
        yield item.load_item()