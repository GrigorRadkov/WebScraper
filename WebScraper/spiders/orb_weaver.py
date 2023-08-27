import json
import scrapy
from scrapy_splash import SplashRequest
from ..items import WebscraperItem
import re

class OrbWeaver(scrapy.Spider):
    name = "orb_weaver"
    allowed_domains = ["shop.mango.com"]
    start_urls = [
        "https://shop.mango.com/bg-en/men/t-shirts-plain/100-linen-slim-fit-t-shirt_47095923.html?c=07",
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url = url, callback = self.parse)
            #yield SplashRequest(url = url, callback = self.parse, args={'wait': 2}, endpoint = 'render.json')

    #Handle main page request, get garment id from url 
    #and construct additional XHR request to get necessary data.
    def parse(self, response):
        self.logger.info("parse: Response from %s", response.url)

        garment_id = re.findall('(\d+).html', response.url)

        xhr_urls = [f"https://shop.mango.com/services/garments/068/en/S/{garment_id[-1]}"]
        for xhr_url in xhr_urls:
            yield scrapy.Request(url = xhr_url, callback = self.parse_xhr_request)

    def parse_xhr_request(self, response):
        self.logger.info("parse_xhr_request: Response from %s", response.url)

        #Instance WebscraperItem to collect json data.
        items = WebscraperItem()

        headers = response.headers
        #print(headers)
        data = json.loads(response.body)
        #print(data)
        
        #default_choice_id = data["colors"]["colors"][0]["id"]

        name    = str(data["name"])
        price   = float(data["price"]["price"])
        colour   = str(data["colors"]["colors"][0]["label"])
        sizes = []
        sizes_json = data["colors"]["colors"][0]["sizes"]
        
        #Collect only available sizes for the default colour.
        for size in sizes_json:
            try:
                if size["available"]:
                    sizes.append(size["label"])
            except KeyError:
                print(f"Item skipped, {size['label']} was unavailable.")

        #sizes   = data["dataLayer"]["ecommerce"]["detail"]["products"][0]["sizeColorAvailability"][default_choice_id]
    
        print(type(name), type(price), type(colour), type(sizes))

        items["name"]   = name
        items["price"]  = price
        items["colour"] = colour
        items["sizes"]  = sizes
        
        #Dump object dict to a json string.
        json_str = json.dumps(items.__dict__['_values'])

        #Write to a json file
        with open('response.json', 'w') as json_file:
            json_file.write(json_str)
            
        #Or just yield items and run with "scrapy crawl orb_weaver -o <filename>.json"
        #yield items
        
