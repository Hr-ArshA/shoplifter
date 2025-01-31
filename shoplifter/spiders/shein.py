import scrapy


class SheinSpider(scrapy.Spider):
    name = "shein"
    allowed_domains = ["us.shein.com"]
    start_urls = ["https://us.shein.com"]

    def parse(self, response):
        pass
