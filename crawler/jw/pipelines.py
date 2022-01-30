# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo

class JwPipeline:
    def process_item(self, item, spider):
        return item


class NewsMongoPipeline:
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db


    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri = crawler.settings.get("MONGO_URI"),
            mongo_db = crawler.settings.get("MONGO_DB")
        )


    def open_spider(self, spider):
        self.cilent = pymongo.MongoClient(self.mongo_uri)
        self.db = self.cilent[self.mongo_db]


    def process_item(self,item,spider):
        # self.db[item["web_name"]].insert(dict(item))
        self.db[item["web_name"]].update({'news_url': item['news_url']}, dict(item), True) #这是关键的去重函数：update 。这里是借助item中的url_token 这个键值对来最为根据，如果dict(item)中已经存在了这个键值对，就不插入。
        return item



    def close_spider(self,spider):
        # self.delete_repeat_data(self.mongo_db["jw"],"news_title") # 去重
        self.cilent.close()