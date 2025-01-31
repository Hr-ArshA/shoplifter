import scrapy
from ..items import ProductItem
from time import sleep


class ZaraSpider(scrapy.Spider):
    name = "zara"
    allowed_domains = ["zara.com"]
    start_urls = ["https://zara.com/us/"]

    redis_key = 'shoplifter:start_urls'

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
                all_products.add(card.css("a.product-link").attrib['href'])
            except:
                pass

        for product in all_products:
            yield response.follow(product, self.product_parse)

    
    def product_parse(self, response):
        item = ProductItem()

        item['url'] = response.request.url
        item["product_id"] = response.request.url.split('-')[-1].split('.')[0][1:]
        sleep(15)

        item['title'] = response.css("h1::text").get()
        item['price'] = response.css("span.money-amount__main::text").get()
        item['description'] = " ".join([i.get() for i in response.xpath("//div[@class='expandable-text__inner-content']/p/text()")])

        if response.css("ul.product-detail-color-selector__color-selector-container") == []:
            if type(response.css("p.product-color-extended-name::text").get()) != None:
                item['color'] = [response.css("p.product-color-extended-name::text").get()]
            else:
                item['color'] = []
        else:
            item['color'] = [i.get() for i in response.css("span.screen-reader-text::text")]


        if response.css("div.size-selector-sizes-size__label::text") == []:
            item['size'] = []
        else:   
            item['size'] = [i.get() for i in response.css("div.size-selector-sizes-size__label::text")]


        pic_list = list()

        for img in response.css("div.media__wrapper"):
            try:
                pic_list.append(img.css("picture source").attrib['srcset'].split(' ')[0].split('?')[0])
        
            except:
                pass
        
        item['pictures'] = pic_list

        print(item)
        yield item