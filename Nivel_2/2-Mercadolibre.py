from scrapy.item import Field,Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor

class Articulo(Item):
    titulo = Field()
    precio = Field()
    descripcion = Field()
    calificacion = Field()

class MercadoLibre(CrawlSpider):
    name = 'Mercado_spider'
    custom_settings = {
        'USER_AGENT' : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
        'CLOSESPIDER_PAGECOUNT': 10 
    }
    #allowed_domains = ["listado.mercadolibre.com.mx","articulo.mercadolibre.com.mx"]
    start_urls = ["https://listado.mercadolibre.com.mx/xiaomi"]

    download_delay = 2

    rules = (
        #Paginación
        Rule(
            LinkExtractor(
                allow = r'_DESDE_'
            ), 
            follow=True
        ),
        #Items
        Rule(
            LinkExtractor(
                allow = r'p/MLM'
            ),
            callback='parse_item',
            follow=True
        )
    )

    def limpiar_descripcion(self, desc):
        new_desc = desc.replace('\n',' ').replace('\t',' ')
        return new_desc

    def parse_precio(self, precio):
        new_precio = precio.replace(',','')
        return int(new_precio)

    def parse_calificacion(self, calif):
        new_calif = calif.replace(',','')
        return float(new_calif)

    def parse_item(self,response):
        sel = Selector(response)
        item = ItemLoader(Articulo(),sel)

        item.add_xpath('titulo','//h1/text()')
        item.add_xpath('precio',
                        '(//div[@class="ui-pdp-price__second-line"])[1]/span[1]/span[@class="andes-money-amount__fraction"]/text()',
                        MapCompose(self.parse_precio))
        item.add_xpath('descripcion','//p[@class="ui-pdp-description__content"]/text()',
                        MapCompose(self.limpiar_descripcion))
        item.add_xpath('calificacion','//span[@class="ui-pdp-review__rating"]/text()',
                        MapCompose(self.parse_calificacion))

        yield item.load_item()