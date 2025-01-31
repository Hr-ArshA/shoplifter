import scrapy
from scrapy_splash import SplashRequest 
from time import sleep
# from scrapy.downloadermiddlewares.retry import get_retry_request
from scrapy.http import Request
import logging

class SheinSpider(scrapy.Spider):
    name = "shein"
    allowed_domains = ["us.shein.com"]
    start_urls = ["https://us.shein.com/"]

    with_out_captcha_url = "https://us.shein.com/ark/2772?goods_id={}&scene=1&pf=google&language=en&siteuid=us&currency=USD&lang=en"

    custom_settings = {
        'FEEDS': {
            'shein.json': {
                'format': 'json',
                'overwrite': True
            }
        }
    }


    def parse(self, response):
        # sleep(10)
        
        tags = response.css("a.bs-nav__cate-link")

        links = set()
        for tag in tags:
            try:
                href = tag.attrib['href']
                links.add(href)
            except:
                pass
        
        for link in links:

            try:
                yield SplashRequest(link, callback=self.category_parse)
            except:
                print(link)



    def category_parse(self, response):
        logging(response)
        print(response.url)
        yield {"product_id":response.url}

