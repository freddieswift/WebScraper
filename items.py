# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

# item to store product data from one page
class ScrapingResultItem(scrapy.Item):
    name=scrapy.Field()
    scraped_items=scrapy.Field()
    price_avg=scrapy.Field()

# item to store results of scraping both pages
# scraped data from both pages will be referenced to same time stamp
class AllScrapedDataItem(scrapy.Item):
    # date and time of scraping
    datetime=scrapy.Field()
    # array of ScrapingResultItem
    data=scrapy.Field()
