import scrapy


class SongteaComSpider(scrapy.Spider):
    name = 'songtea_com'
    allowed_domains = ['songtea.com']
    start_urls = ['http://songtea.com/']

    def parse(self, response):
        pass
