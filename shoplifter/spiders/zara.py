import scrapy
from ..items import ProductItem
from time import sleep
import json
from scrapy.exceptions import IgnoreRequest
from captcha_solver import solve_captcha 


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

    # Handle errors like 404, 500, etc.
    handle_httpstatus_list = [404, 500, 403, 429]


    def parse(self, response):
        # Check if the page contains a CAPTCHA challenge
        if self._is_captcha_page(response):
            print("CAPTCHA detected!")
            # Extract the site_key (you need to adapt this part based on the website you're crawling)
            site_key = self._get_site_key(response)
            site_url = response.url
            
            # Solve the CAPTCHA using Anti-Captcha
            captcha_solution = solve_captcha(site_url, site_key)
            
            if captcha_solution:
                # Submit the CAPTCHA solution and continue scraping
                yield scrapy.FormRequest(
                    url=site_url,
                    formdata={'g-recaptcha-response': captcha_solution},
                    callback=self.after_captcha
                )
            else:
                print("Failed to solve CAPTCHA.")
                return

        else:
            # Proceed with the regular scraping
            self.parse_products(response)

    
    def _is_captcha_page(self, response):
        # Check if the response page contains a CAPTCHA challenge.
        return 'recaptcha' in response.text.lower()
    
    def _get_site_key(self, response):
        # Extract the reCAPTCHA site key from the page.
        site_key = response.xpath('//div[@class="g-recaptcha"]/@data-sitekey').get()
        return site_key
    
    def after_captcha(self, response):
        # Handle the page after the CAPTCHA is solved.
        print("CAPTCHA bypassed successfully, continue scraping.")

        self.parse_pages(response)


    def parse_pages(self, response):
        if response.status == 404:
            self.logger.error(f"Page not found: {response.url}")
            return  IgnoreRequest
        elif response.status == 429:
            self.logger.warning(f"Rate limit exceeded: {response.url}")
            return  self.retry_request(response)
        elif response.status == 500:
            self.logger.error(f"Server error: {response.url}")
            return  self.retry_request(response)
        
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

        item['title'] = response.css(self.config['title']['css']).get()
        item['price'] = response.css(self.config['price']['css']).get()

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


    def retry_request(self, response):
        # Create a new request with the same URL but force retry logic
        retries = response.meta.get('retry_times', 0) + 1
        if retries <= self.settings.get('RETRY_TIMES'):
            self.logger.info(f"Retrying {response.url} (attempt {retries})")
            return scrapy.Request(response.url, callback=self.parse, errback=self.errback, dont_filter=True, meta={'retry_times': retries})
        else:
            self.logger.error(f"Max retries reached for {response.url}")
            return None