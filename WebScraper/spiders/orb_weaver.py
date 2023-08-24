import scrapy

class OrbWeaver(scrapy.Spider):
    name = "orb_weaver"
    allowed_domains = ["shop.mango.com"]
    start_urls = [
        "https://shop.mango.com/bg-en/men/t-shirts-plain/100-linen-slim-fit-t-shirt_47095923.html?c=07",
    ]

    def parse(self, response):
        self.logger.info("Response from %s", response.url)
        name   = response.css("title::text").extract()
        #price  = response.css("span::text").extract()
        #colour = response.css("micro-frontend").extract()
        #size   = response.css("title").extract()

        yield {"name" : name}
        #yield {"price" : price}
        #yield {"colour" : colour}
        