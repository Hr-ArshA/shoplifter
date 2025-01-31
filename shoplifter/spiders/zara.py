import scrapy
from ..items import ProductItem
from time import sleep
import json


class ZaraSpider(scrapy.Spider):
    name = "zara"
    allowed_domains = ["zara.com"]
    start_urls = ["https://zara.com/us/"]

    redis_key = 'shoplifter:start_urls'

    with open('config.json', 'r') as f:
        config = json.load(f)['zara']

    custom_settings = {
        'FEEDS': {
            'zara.json': {
                'format': 'json',
                'overwrite': True
            }
        }
    }


    def parse(self, response):
        carousel = response.css("div.zds-carousel-content ul")

        all_pages = set()
        for ul in carousel:
            for a in ul.css('a'):
                try:
                    all_pages.add(a.attrib['href'])
                except:
                    pass

        for page in all_pages:
            yield response.follow(page, self.page_parse)


    def page_parse(self, response):
        cards = response.css("div.product-grid-product__figure")

        all_products = set()

        for card in cards:
            try:
                all_products.add(card.css(self.config['url']['css']).attrib['href'])
            except:
                pass

        for product in all_products:
            yield response.follow(product, self.product_parse)

    
    def product_parse(self, response):
        item = ProductItem()

        item['url'] = response.request.url
        item["product_id"] = response.request.url.split('-')[-1].split('.')[0][1:]
        sleep(20)

        item['title'] = response.css(self.config['title']['css']).get()
        item['price'] = response.css(self.config['price'['css']]).get()

        # Extracting description text from HTML structure and pasting them together
        item['description'] = " ".join([i.get() for i in response.xpath(self.config['description']['xpath'])])

        # Extracting colors from HTML structure
        if response.css(self.config['color']['css']) == []:
            if type(response.css("p.product-color-extended-name::text").get()) != None:
                item['color'] = [response.css("p.product-color-extended-name::text").get()]
            else:
                item['color'] = []
        else:
            item['color'] = [i.get() for i in response.css("span.screen-reader-text::text")]

        # Extracting size from HTML structure
        if response.css(self.config['size']['css']) == []:
            item['size'] = []
        else:   
            item['size'] = [i.get() for i in response.css(self.config['size']['css'])]

        # Extracting photos and adding them to the list
        item['pictures'] = [str(i).split(' ')[0].split('?')[0] for i in response.css(self.config['images']['css'])]

        yield item