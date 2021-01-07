import scrapy
from scrapy.crawler import CrawlerProcess
import re

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
            'company_tea_category',
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
            category_tea = response.xpath(Locators.CATEGORIES + f'{[i]}')
            tea_category = category_tea.xpath(Locators.TEA_CATEGORY)
            items['tea_category'] = tea_category
            less_price = 0
            for tea in category_tea:
                price = float(tea.xpath(Locators.PRICE_USD).get().strip().split('$')[1])
                if price < less_price:
                    price_usd = price
                    tea_name = tea.xpath(Locators.TEA_NAME).get()
                    tea_url = 'https://songtea.com/' + tea.xpath(Locators.TEA_URL).get()
                    items['price_usd'] = price_usd
                    items['tea_name'] = tea_name
                    items['tea_url'] = tea_url
                    less_price = price

            yield scrapy.Request(items['tea_url'], callback=self.parse_tea,
                                 cb_kwargs={

                                 })



                # # amount_g = category.xpath(Locators.AMOUNT_G).get()
                # # amount_tea_bags = category.xpath(Locators.AMOUNT_TEA_BAGS).get()
                # product_page_link = category.xpath(Locators.PRODUCT_PAGE_LINK).get()
                # # company_home_page = category.xpath(Locators.COMPANY_HOME_PAGE).get()
                # if less_price <= price_usd:
                #     price_usd = float(tea.xpath(Locators.PRICE_USD).get().strip().split('$')[1])
                #     tea_name = category.xpath(Locators.TEA_NAME).get()
                #     # amount_g = category.xpath(Locators.AMOUNT_G).get()
                #     # amount_tea_bags = category.xpath(Locators.AMOUNT_TEA_BAGS).get()
                #     product_page_link = category.xpath(Locators.PRODUCT_PAGE_LINK).get()
                #     # company_home_page = category.xpath(Locators.COMPANY_HOME_PAGE).get()
                #     # items['amount_g'] = amount_g
                #     # items['amount_tea_bags'] = amount_tea_bags
                #     items['product_page_link'] = product_page_link
                #     # items['company_home_page'] = response.url
                #
                # yield items


if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(SongteaComSpider)
    process.start()
