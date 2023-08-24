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
        script  = response.css("script").re_first(r"\"salePrice\":[0-9]+.[0-9]+")
        #colour = response.css("micro-frontend").extract()
        #size   = response.css("title").extract()

        yield {"name" : name}
        yield {"script" : script}
        #yield {"colour" : colour}
        