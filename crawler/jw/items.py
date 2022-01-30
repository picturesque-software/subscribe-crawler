# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    web_name = scrapy.Field() # 网站名称
    news_source_code = scrapy.Field() # 新闻网页源码
    news_author = scrapy.Field() # 新闻发布者
    news_title = scrapy.Field() # 新闻标题
    news_pub_time = scrapy.Field() # 新闻发布时间
    news_cat = scrapy.Field()  # 新闻类别，enum(教学动态，公告通知)
    news_url = scrapy.Field() # 新闻地址
    news_visit = scrapy.Field() # 新闻访问量
    update_time = scrapy.Field() # 更新时间
    pass
