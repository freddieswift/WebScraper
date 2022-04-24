import scrapy
from ssc_project.items import ScrapingResultItem
from ssc_project.items import AllScrapedDataItem
import datetime

class SscSpider(scrapy.Spider):
    name = 'ssc'
    allowed_domains = ['etsy.com']
    
    def start_requests(self):

        # AllScrapedData item is passed through the multiple parsing method
        # This item is eventually passed to the pipeline in parse_second()
        # to be stored in the database

        # initialise data field as an array to store both
        # ScrapingResultItems

        AllScrapedData = AllScrapedDataItem()
        AllScrapedData['data'] = []

        # create request for sheringham socks company
        # pass AllScrapedData item as an arguament to be accessed
        # in the callback
        # pass the name argument so the scraping results for this page
        # can be obtained in the front end

        sscRequest = scrapy.Request(
            'https://www.etsy.com/uk/shop/thesheringhamsockco',
            self.parse_first
        )
        sscRequest.cb_kwargs['AllScrapedData'] = AllScrapedData
        sscRequest.cb_kwargs['name'] = 'ssc'

        yield sscRequest

    def parse_first(self, response, name, AllScrapedData):

        # scrape the product information from the response
        # product information is returned as a ScrapingResultItem
        scrapingResult = self.get_product_info(response, name)

        # add scraping result item to array in AllScrapedData
        AllScrapedData['data'].append(scrapingResult)
        
        # create request for saints socks
        # pass AllScrapedData item that contains the previous ScrapingResultItem
        # pass name argument 
        saintsRequest = scrapy.Request(
            'https://www.etsy.com/uk/shop/SaintsSocks',
             self.parse_second
        )
        saintsRequest.cb_kwargs['name'] = 'saints'
        saintsRequest.cb_kwargs['AllScrapedData'] = AllScrapedData
        yield saintsRequest

    def parse_second(self, response, name, AllScrapedData):

        # scrape the product information from the response
        scrapingResult = self.get_product_info(response, name)

        # add ScrapingResultItem to array in AllScrapedData
        AllScrapedData['data'].append(scrapingResult)

        # add timestamp tp AllScrapedData
        # both scraping results will be referenced to the same timestamp
        AllScrapedData['datetime'] = datetime.datetime.now().replace(microsecond=0)

        # pass AllScrapedData to pipeline to store in db
        yield AllScrapedData

    def get_product_info(self, response, name):

        # extract titles and prices of products
        titles = response.css('.v2-listing-card__title::text').extract()
        prices = response.css('.currency-value::text').extract()

        scraped_items = []
        price_count = 0

        # create an object containing title and price of each product
        # and append to scraped items
        for item in zip(titles, prices):
            scraped_info = {
                'title':item[0].strip(),
                'price':float(item[1].strip()),
            }

            price_count += float(item[1].strip())

            scraped_items.append(scraped_info)
        
        price_avg = round(price_count / (len(scraped_items)), 2)

        # create ScrapingResultItem that contains name of seller (passed in as argument)
        # the scraped items from the page and the average price
        scrapingResult = ScrapingResultItem(
            name=name,
            scraped_items=scraped_items,
            price_avg=price_avg,
        )
        
        return scrapingResult


## AllScrapedData working version

# class SscSpider(scrapy.Spider):
#     name = 'ssc'
#     allowed_domains = ['etsy.com']
#     #start_urls = ['https://www.etsy.com/uk/shop/thesheringhamsockco', 'https://www.etsy.com/uk/shop/SaintsSocks']

#     def start_requests(self):

#         AllScrapedData = AllScrapedDataItem()
#         AllScrapedData['data'] = []

#         sscRequest = scrapy.Request(
#             'https://www.etsy.com/uk/shop/thesheringhamsockco',
#             self.parse
#         )
#         sscRequest.cb_kwargs['AllScrapedData'] = AllScrapedData
#         sscRequest.cb_kwargs['name'] = 'ssc'

#         yield sscRequest
        

    

#     def parse(self, response, name, AllScrapedData):

#         titles = response.css('.v2-listing-card__title::text').extract()
#         prices = response.css('.currency-value::text').extract()

#         scraped_items = []
#         price_count = 0

#         for item in zip(titles, prices):
#             scraped_info = {
#                 'title':item[0].strip(),
#                 'price':float(item[1].strip()),
#             }

#             price_count += float(item[1].strip())

#             scraped_items.append(scraped_info)
        
#         price_avg = round(price_count / (len(scraped_items)), 2)

#         scrapingResult = ScrapingResultItem(
#             name=name,
#             scraped_items=scraped_items,
#             price_avg=price_avg,
#         )

#         AllScrapedData['data'].append(scrapingResult)
        
#         saintsRequest = scrapy.Request('https://www.etsy.com/uk/shop/SaintsSocks', self.parse)
#         saintsRequest.cb_kwargs['name'] = 'saints'
#         saintsRequest.cb_kwargs['AllScrapedData'] = AllScrapedData
#         yield saintsRequest

#         AllScrapedData['datetime'] = datetime.datetime.now()

#         yield AllScrapedData


# class SscSpider(scrapy.Spider):
#     name = 'ssc'
#     allowed_domains = ['etsy.com']
#     #start_urls = ['https://www.etsy.com/uk/shop/thesheringhamsockco', 'https://www.etsy.com/uk/shop/SaintsSocks']

#     def start_requests(self):
#         #generate random number in range 0, 1,000,000 - date time placeholder
#         seed(1)

#         datetime = randint(0, 1000000)

#         sscRequest = scrapy.Request('https://www.etsy.com/uk/shop/thesheringhamsockco', self.parse)
#         sscRequest.cb_kwargs['name'] = 'ssc'
#         sscRequest.cb_kwargs['datetime'] = datetime

#         saintsRequest = scrapy.Request('https://www.etsy.com/uk/shop/SaintsSocks', self.parse)
#         saintsRequest.cb_kwargs['name'] = 'saints'
#         saintsRequest.cb_kwargs['datetime'] = datetime

#         yield sscRequest
#         yield saintsRequest
        

#     def parse(self, response, name, datetime):

#         titles = response.css('.v2-listing-card__title::text').extract()
#         prices = response.css('.currency-value::text').extract()

#         scraped_items = []
#         price_count = 0

#         for item in zip(titles, prices):
#             scraped_info = {
#                 'title':item[0].strip(),
#                 'price':float(item[1].strip()),
#             }

#             price_count += float(item[1].strip())

#             scraped_items.append(scraped_info)
        
#         price_avg = round(price_count / (len(scraped_items)), 2)

#         scrapingResult = ScrapingResultItem(
#             datetime=datetime,
#             name=name,
#             scraped_items=scraped_items,
#             price_avg=price_avg,
#         )

#         yield scrapingResult


#class SscSpider(scrapy.Spider):
#     name = 'ssc'
#     allowed_domains = ['etsy.com']
#     start_urls = ['www.store.com/seller1', 'www.store.com/seller2']

#     def parse(self, response):

#         titles = response.css('.v2-listing-card__title::text').extract()
#         prices = response.css('.currency-value::text').extract()

#         scraped_items = []
#         price_count = 0

#         for item in zip(titles, prices):
#             scraped_info = {
#                 'title':item[0].strip(),
#                 'price':float(item[1].strip()),
#             }

#             price_count += float(item[1].strip())

#             scraped_items.append(scraped_info)
        
#         price_avg = round(price_count / (len(scraped_items)), 2)

#         scrapingResult = ScrapingResultItem(
#             name=self.name,
#             scraped_items=scraped_items,
#             price_avg=price_avg,
#         )

#         yield scrapingResult


 # def start_requests(self):
    #     sscData = scrapy.Request('https://www.etsy.com/uk/shop/thesheringhamsockco', self.parse)
    #     saintsData = scrapy.Request('https://www.etsy.com/uk/shop/SaintsSocks', self.parse)

    #     # yield scrapy.Request('https://www.etsy.com/uk/shop/thesheringhamsockco', self.parse)
    #     # yield scrapy.Request('https://www.etsy.com/uk/shop/SaintsSocks', self.parse)


    #     scrapedData = ScrapedDataItem(
    #         datetime=datetime.datetime.now(),
    #         data=[sscData, saintsData]
    #     )
    #     return scrapedData
















# import scrapy
# from ssc_project.items import SscItem
# import datetime

# class SscSpider(scrapy.Spider):
#     name = 'ssc'
#     allowed_domains = ['etsy.com']
#     start_urls = ['https://www.etsy.com/uk/shop/thesheringhamsockco']

#     def parse(self, response):

#         titles = response.css('.v2-listing-card__title::text').extract()
#         prices = response.css('.currency-value::text').extract()


#         scraped_items = []
#         price_count = 0

#         for item in zip(titles, prices):
#             scraped_info = {
#                 'title':item[0].strip(),
#                 'price':float(item[1].strip()),
#             }

#             price_count += float(item[1].strip())
            
#             scraped_items.append(scraped_info)
        
#         price_avg = round(price_count / (len(scraped_items)), 2)

#         sscItem = SscItem(
#             name=self.name,
#             datetime=datetime.datetime.now(),
#             scraped_items=scraped_items,
#             price_avg=price_avg,
#         )

#         yield sscItem

        
