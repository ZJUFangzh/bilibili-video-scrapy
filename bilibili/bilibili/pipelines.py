# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
import scrapy

from scrapy.exceptions import DropItem


class MongoPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB')

        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient()
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        # self.db[item.collection].insert(dict(item))
        # 查重
        self.db[item.collection].update({'aid': item['aid']}, {
            '$set': item}, True)
        return item

    def clost_spider(self, spider):
        self.client.close()
