import scrapy
from scrapy.crawler import CrawlerProcess
import re
import json

from ii_tea_prices.i_tea_prices.spiders.songtea_com_locators import Locators
from ii_tea_prices.i_tea_prices.items import SongTeaItem


class SongteaComSpider(scrapy.Spider):
    name = 'songtea_com'
    start_urls = ['https://songtea.com/pages/tea-by-type']

    custom_settings = {
        'FEED_EXPORT_BATCH_ITEM_COUNT': 100,
        'FEED_FORMAT': 'csv',
        'FEED_URI': f"../../iii_results/%(batch_id)02d-{'_'.join(re.findall(r'[A-Z][^A-Z]*', __qualname__)[:-1]).lower()}.csv",
        'FEED_EXPORT_FIELDS': [
            'company',
            'tea_category',
            'tea_name',
            'price_usd',
            'amount_g',
            'amount_tea_bags',
            'product_page_link',
            'company_home_page',
        ]
    }

    def parse(self, response, **kwargs):
        items = SongTeaItem()

        company = 'Song Tea'
        items['company'] = company
        categories = response.xpath(Locators.CATEGORIES)
        for i in range(1, len(categories) + 1):
            category = response.xpath(f'{Locators.CATEGORIES}{[i]}')
            tea_category = category.xpath(Locators.TEA_CATEGORY).get()
            items['tea_category'] = tea_category
            category_tea = category.xpath(f'{Locators.CATEGORIES}{[i]}{Locators.TEA}')
            prices = []
            for tea in category_tea:
                price = float(tea.xpath(Locators.PRICE_USD).re_first(r'(\d+\.\d+)'))
                prices.append(price)
            less_price_index = prices.index(min(prices)) + 1
            price_usd = min(prices)
            items['price_usd'] = price_usd
            tea_name = response.xpath(f'({Locators.CATEGORIES}{[i]}{Locators.TEA_NAME}){[less_price_index]}/text()').get()
            items['tea_name'] = tea_name
            company_home_page = 'https://songtea.com'
            items['company_home_page'] = company_home_page
            product_page_link = company_home_page + response.xpath(f'({Locators.CATEGORIES}{[i]}{Locators.PRODUCT_PAGE_LINK}){[less_price_index]}/@href').get()
            items['product_page_link'] = product_page_link

            yield scrapy.Request(items['product_page_link'], callback=self.parse_tea, cb_kwargs=items)

    @staticmethod
    def parse_tea(response, **kwarg):
        items = kwarg
        data = json.loads(response.xpath(Locators.JSON_FILE).get())
        amount_g = data['variants'][0]['title'].split(' ')[0]
        items['amount_g'] = amount_g
        if amount_g:
            items['amount_tea_bags'] = None
        return items


if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(SongteaComSpider)
    process.start()
