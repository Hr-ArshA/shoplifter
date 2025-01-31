import scrapy
from scrapy_splash import SplashRequest 
from time import sleep
from scrapy.http import Request
import logging
from scrapy.exceptions import IgnoreRequest
from captcha_solver import solve_captcha 

class SheinSpider(scrapy.Spider):
    name = "shein"
    allowed_domains = ["us.shein.com"]
    start_urls = ["https://us.shein.com/"]

    with_out_captcha_url = "https://us.shein.com/ark/2772?goods_id={}&scene=1&pf=google&language=en&siteuid=us&currency=USD&lang=en"

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

