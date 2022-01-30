# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo
import pymysql

class SubscribePipeline:
    def process_item(self, item, spider):
        return item


class SubscribeMongoPipeline:
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
        # self.db[item["web_name"]].update({'news_url': item['news_url']}, dict(item), True) 
        self.db[item["web_name"]].update_one({"news_url": item['news_url']},{"$setOnInsert":dict(item)},upsert=True)
        return item



    def close_spider(self,spider):
        # self.delete_repeat_data(self.mongo_db["jw"],"news_title") # 去重
        self.cilent.close()

class SubscribeMysqlPipeline:
    def __init__(self, host, database, user, password, port, cursorclass=pymysql.cursors.DictCursor):
        self.host =host
        self.database = database
        self.user = user
        self.password = password
        self.port = port # port其实是默认的

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host = crawler.settings.get("MYSQL_HOST"),
            database = crawler.settings.get("MYSQL_DATABASE"),
            user = crawler.settings.get("MYSQL_USER"),
            password = crawler.settings.get("MYSQL_PASSWORD"),
            port = crawler.settings.get("MYSQL_PORT"),
        )
    

    def open_spider(self,spider):
        # 注意：最新版本 MYSQL需要指明参数名
        self.db = pymysql.connect(host=self.host,user=self.user,password=self.password,database=self.database,port=self.port,charset="utf8mb4")  # charset="utf-8",不要加
        self.cursor = self.db.cursor()

    def close_spider(self,spider):
        self.db.close()

    def process_item(self, item, spider):
        print("mysql inserting!")
        data = dict(item)
        keys = ", ".join(data.keys())
        values = ", ".join(['%s']*len(data))
        sql = 'insert into %s (%s) values (%s) ' %(item.table,keys,values)
        self.cursor.execute(sql, tuple(data.values()))
        self.db.commit()
        return item 