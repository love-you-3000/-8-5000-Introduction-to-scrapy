# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem

# class TutorialPipeline(object):
#     def process_item(self, item, spider):
#         return item

class TextPipeline(object):
    def __init__(self):
        self.limit = 50 # 定义爬取文本的长度限制

    def process_item(self, item, spider):
        """
        每个实现保存的类里面必须都要有这个方法,且名字固定,用来具体实现怎么保存
        """
        if item['text']:
            if len(item['text'])> self.limit:  #　如果文本超过了定义的限制,就将文本超过的部分修改为省略号
                item['text'] = item['text'][0:self.limit].rstrip()+'...'
            return item
        else:
            return DropItem('Missing Text')

import pymongo

class MongoPipline(object):
    def __init__(self,mongo_uri,mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls,crawler):
        """
        scrapy为我们访问settings提供了这样的一个方法,这里,
        我们需要从settings.py文件中,取得数据库的URI和数据库名称
        """
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db = crawler.settings.get('MONGO_DB')
        )

    def open_spider(self,spider):
        """
        爬虫一旦开启,就会实现这个方法,连接到数据库
        """
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def process_item(self,item,spider):
        """
        每个实现保存的类里面必须都要有这个方法,且名字固定,用来具体实现怎么保存
        """
        name = item.__class__.__name__  # 将表名定义成item的类名,即QuoteItem
        self.db[name].insert(dict(item))
        return item

    def close_spider(self,spider):
        """
        爬虫一旦开启,就会实现这个方法,连接到数据库
        """
        self.client.close()