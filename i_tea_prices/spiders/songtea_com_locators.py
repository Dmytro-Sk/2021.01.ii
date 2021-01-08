class Locators:

    """Page 1"""
    
    # main locators
    TEA_CATEGORY = './/h1/text()'
    TEA_NAME = '//p[1]'
    PRICE_USD = './/p[2]/text()'
    PRODUCT_PAGE_LINK = '//a'


    # additional locators
    CATEGORIES = '(//div[@id="CollectionSection"]/div[position()>2])'
    TEA = '//div[@class="grid__item large--one-half"]'

    """Page 2"""

    # main locators

    # additional locators
    JSON_FILE = '//*[@id="ProductJson-product-template"]/text()'
