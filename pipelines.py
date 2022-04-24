# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymongo
from itemadapter import ItemAdapter

class MongoDBPipeline:

    def __init__(self, mongo_uri, mongo_db, mongo_coll):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.mongo_coll = mongo_coll

    # This class method is called to create a pipeline instance from a crawler
    # Provide access to settings
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get("MONGO_URI"),
            mongo_db=crawler.settings.get("MONGO_DATABASE", 'sscDatabase'),
            mongo_coll=crawler.settings.get("MONGO_COLL", 'scapingResult'),
        )

    #This method is called when the spider is triggered
    #Must take in the spider object
    def open_spider(self, spider):
        #connect to mongodb when spider is opened
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.collection = self.db[self.mongo_coll]
    
    #this method is called when the spider is closed
    def close_spider(self, spider):
        #close the connection to mongodb
        self.client.close()
    
    # this method process the item returned by the spider
    # and inserts it into the db
    def process_item(self, item, spider):
        # item adaptor is used to convert result to dict to store in db
        result_dict = ItemAdapter(item).asdict()
        self.collection.insert_one(result_dict)
        return item