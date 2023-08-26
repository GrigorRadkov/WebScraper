import scrapy
from scrapy_splash import SplashRequest

class OrbWeaver(scrapy.Spider):
    name = "orb_weaver"
    #allowed_domains = ["shop.mango.com"]
    start_urls = [
        "https://shop.mango.com/bg-en/men/t-shirts-plain/100-linen-slim-fit-t-shirt_47095923.html?c=07",
    ]

    def start_requests(self):
        
        for url in self.start_urls:
            yield scrapy.Request(url = url, callback = self.parse)
            #yield SplashRequest(url = url, callback = self.parse)


    def parse(self, response):
        self.logger.info("Response from %s", response.url)
        #name   = response.css("title::text").extract()
        #script  = response.css("script").re_first(r"\"salePrice\":([0-9]+.[0-9]+)")
        #colour = response.css("script").extract(r"\"salePrice\":([0-9]+.[0-9]+)")
        #size   = response.css("script").extract(r"\"sizeAvailability\":([a-Z]+.[a-Z]+)")
        #price = response.css("span").extract()

        #yield   {"name" : name,
        #        "script" : script,
        #        "price" : price
        #        }
        with open('page.html', 'wb') as html_file:
            html_file.write(response.body)