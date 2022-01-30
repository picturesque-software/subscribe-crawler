from requests.api import get
import scrapy
from jw.items import NewsItem
import requests
import bs4
from retry import retry
import time
import random
from time import sleep
from urllib.parse import urlencode
import urllib3
urllib3.disable_warnings()
import re

headers = {
    "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Mobile Safari/537.36"
}
@retry(tries=3, delay=random.randint(1, 2))
def get_response(url):
    """通用api"""
    response = requests.get(url,headers=headers,verify=False)
    while response.status_code != 200:
        print("reconnect")
        response = requests.get(url,headers=headers,verify=False)
        sleep(2)
        
    soup = bs4.BeautifulSoup(response.content.decode("utf-8"),"lxml")
    
    return soup


class SbcSpiderSpider(scrapy.Spider):
    name = 'sbc_spider'
    allowed_domains = ['sbc.nju.edu.cn']
    start_urls = ['https://sbc.nju.edu.cn/xwdt/20210712/i204260.html']

    def parse(self, response):
        item = NewsItem()
        item['web_name'] = "sbc"
        item['news_source_code'] = response.text
        item['news_author'] = "实验室与设备管理处"
        item['news_title']= response.xpath("//h1[@class='title']//text()").extract_first("未知")
        item['news_pub_time'] = response.xpath("//span[@class='time']//text()").extract_first("未知")
        item["news_url"] = response.url
        item["update_time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # item['news_cat'] = '' # 暂不分类
        yield item
        
        self.start_requests()

    
    def start_requests(self):
        # 新闻动态
        xwdt_url = "https://sbc.nju.edu.cn/xwdt/index.html"
        # 通知公告
        tzgg_url = "https://jw.nju.edu.cn/_s414/24774/list1.psp"
        # 报废信息公示
        bfxx_url = "https://sbc.nju.edu.cn/bfxxgs/index.html"
        # 其他公示
        qtgs_url = "https://sbc.nju.edu.cn/qtgs/index.html"
        # 实验教学中心
        syjx_url = "https://sbc.nju.edu.cn/syjxzx/index.html"


        xwdt_soup = get_response(xwdt_url)
        tzgg_soup = get_response(tzgg_url)
        bfxx_soup = get_response(bfxx_url)
        qtgs_soup = get_response(qtgs_url)
        syjx_soup = get_response(syjx_url)

        xwdt_news_url_list = re.findall('"url":"(.*?)"',str(xwdt_soup.find(class_="right_list")))
        tzgg_news_url_list = re.findall('"url":"(.*?)"',str(tzgg_soup.find(class_="right_list")))
        bfxx_news_url_list = re.findall('"url":"(.*?)"',str(bfxx_soup.find(class_="right_list")))
        qtgs_news_url_list = re.findall('"url":"(.*?)"',str(qtgs_soup.find(class_="right_list")))
        syjx_news_url_list = re.findall('"url":"(.*?)"',str(syjx_soup.find(class_="right_list")))

        # base_url = "https://jw.nju.edu.cn/"
        for news_url in xwdt_news_url_list+tzgg_news_url_list+bfxx_news_url_list+qtgs_news_url_list+syjx_news_url_list:
            print("***tesing***:" + str(len(xwdt_news_url_list))+str(len(tzgg_news_url_list))+str(len(bfxx_news_url_list))+str(len(qtgs_news_url_list))+str(len(syjx_news_url_list)))
            yield scrapy.Request(news_url, self.parse)