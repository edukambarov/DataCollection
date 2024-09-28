# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
from pprint import pprint

class UsmallParserPipeline:

    # def __init__(self):
    #     client = MongoClient('localhost',27017)
    #     self.mongo_base = client.sneakers
    #
    # def process_item(self, item, spider):
    #     collection = self.mongo_base[spider.name]
    #     collection.insert_one(item)
    #     # pprint(item)
    #     return item

    pass
