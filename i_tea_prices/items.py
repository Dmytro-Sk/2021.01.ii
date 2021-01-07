# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SongTeaItem(scrapy.Item):
    company = scrapy.Field()
    tea_category = scrapy.Field()
    tea_name = scrapy.Field()
    price_usd = scrapy.Field()
    amount_g = scrapy.Field()
    amount_tea_bags = scrapy.Field()
    product_page_link = scrapy.Field()
    company_home_page = scrapy.Field()

    tea_url = scrapy.Field()
