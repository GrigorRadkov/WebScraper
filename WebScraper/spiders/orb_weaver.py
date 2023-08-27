import json
import scrapy
from scrapy_splash import SplashRequest
from ..items import WebscraperItem

class OrbWeaver(scrapy.Spider):
    name = "orb_weaver"
    #allowed_domains = ["shop.mango.com"]
    start_urls = [
        #"https://shop.mango.com/bg-en/men/t-shirts-plain/100-linen-slim-fit-t-shirt_47095923.html?c=07",
        "https://shop.mango.com/services/garments/068/en/S/4709592307",
    ]

    def start_requests(self):
        
        for url in self.start_urls:
            yield scrapy.Request(url = url, callback = self.parse)
            #yield SplashRequest(url = url, callback = self.parse, args={'wait': 2}, endpoint = 'render.json')


    """ def parse(self, response):
        self.logger.info("parse: Response from %s", response.url)

        xhr_urls = ["https://shop.mango.com/services/garments/068/en/S/4709592307"]
        for xhr_url in xhr_urls:
            yield SplashRequest(url = xhr_url, callback = self.parse_micro_frontend) """

    def parse(self, response):
        self.logger.info("parse_micro_frontend: Response from %s", response.url)

        items = WebscraperItem()

        headers = response.headers
        #print(headers)
        data = json.loads(response.body)
        #print(data)
        
        #default_choice_id = data["colors"]["colors"][0]["id"]

        name    = str(data["name"])
        price   = float(data["price"]["price"])
        color   = str(data["colors"]["colors"][0]["label"])
        sizes = []
        sizes_json = data["colors"]["colors"][0]["sizes"]
        
        for size in sizes_json:
            try:
                if size["available"]:
                    sizes.append(size["label"])
            except KeyError:
                print(f"Item skipped, {size['label']} was unavailable.")

        #sizes   = data["dataLayer"]["ecommerce"]["detail"]["products"][0]["sizeColorAvailability"][default_choice_id]
    
        print(type(name), type(price), type(color), type(sizes))

        items["name"]   = name
        items["price"]  = price
        items["color"]  = color
        items["sizes"]  = sizes
        
        json_str = json.dumps(items.__dict__['_values'])

        #Or just yield items and run with "scrapy crawl orb_weaver -o <filename>.json"
        #yield items
        
        with open('response.json', 'w') as json_file:
            json_file.write(json_str)