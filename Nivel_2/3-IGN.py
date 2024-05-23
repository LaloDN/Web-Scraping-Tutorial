#Para este ejercicio, se utilizará la página IGN, habrá dos dimensiones: el tipo de página, y la paginación
#Para los tipos de página tenemos: noticias, reseñas y videos, para las noticias extraeremos el título y el texto de esta,
#para las reseñas el título y la calificación de la reseña, de los videos el título y la fecha de publicación

from scrapy.item import Item, Field
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose


#Abstracciones
class Noticia(Item):
    titulo = Field()
    texto = Field()

class Reseña(Item):
    titulo = Field()
    calificacion = Field()

class Video(Item):
    titulo = Field()
    fecha = Field()

class IGNCrawler(CrawlSpider):
    name = 'ign'
    
    custom_settings = {
        'USER_AGENT' : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
        'CLOSESPIDER_PAGECOUNT': 100
    }

    #Recuerda que allowed domains es para que el spider no de click en vínculos que nos lleven a otros lados
    #Tanto las páginas de reseñas, noticias y videos tienen en común este dominio
    allowed_domains = ['latam.ign.com']

    download_delay = 2

    #Aquí empezará la búsqueda
    start_urls=['https://latam.ign.com/se/?q=crash&order_by=&model=article']

    """
    Para este ejercicio necesitamos 5 reglas:
    1-La primera para navegar entre las tabs, así iremos a la tab de noticias, la tab de reseñas y la de vídeos
    2-La segunda sería una regla para meterse a una página de noticias
    3-La tercera lo mismo que la segunda, pero para reseñas
    4-Lo mismo con al de vídeos
    5-Por último, necesitamos una regla que nos ayude a viajar por la paginación
    """
    rules = (
        #Tabs
        Rule(
            #Esta rule no tiene callback porque no voy a extraer info. solo voy a navegar por ahí
            LinkExtractor(
                allow=r'type='
            ), follow=True
        ),
        #Paginación
        Rule(
            LinkExtractor(
                allow=r'page=\d+' #Recuerda que el \d+ significa un número cualquiera
            ), follow=True
        ),
       
        #Noticias
        Rule(
            LinkExtractor(
                allow=r'/news/'
            ), follow=True, callback='parse_news'
        ),

        #Reseñas
        Rule(
            LinkExtractor(
                allow=r'/review/'
            ), follow=True, callback='parse_reivews'
        ),
        
        #Vídeos
        Rule(
            LinkExtractor(
                allow=r'/video/'
            ), follow=True, callback='parse_videos'
        )
    )


    def parse_news(self, response):
        item = ItemLoader(Noticia(),response)
        item.add_xpath('titulo','//h1[@id="id_title"]/text()')
        item.add_xpath('texto','//div[@id="id_text"]//*/text()') #El asterísco significa cualquier tag

        yield item.load_item()

    def parse_reviews(self, response):
        item = ItemLoader(Reseña(),response)
        item.add_xpath('titulo','//h1/text()')
        item.add_xpath('calificacion','(//span[@class="side-wrapper side-wrapper hexagon-content"])[1]/div/text()')

        yield item.load_item()

    def parse_videos(self, response):
        item = ItemLoader(Video(),response)
        item.add_xpath('titulo','//h1/text()')
        item.add_xpath('fecha','//span[@class="publish-date"]/text()')

        yield item.load_item()

