from requests.api import get
import scrapy
from subscribe.items import SubscribeItem
import requests
import bs4
import os
import re
from retry import retry
import random
from urllib.parse import urlencode
from time import sleep
import time
from hashlib import md5
from urllib import parse
import urllib3
urllib3.disable_warnings()

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
        item = SubscribeItem()
        item['web_name'] = "sbc"
        item['news_author'] = "实验室与设备管理处"
        domain = parse.urlparse(response.url).scheme + "://" + parse.urlparse(response.url).netloc
        item['news_source_code'] =  "<meta charset='utf8'> \n" + re.sub('src="/','src="{0}/'.format(domain),response.xpath("//div[@class='right_list wenzhang_contain_1']").extract_first())
        item['news_title']= response.xpath("//h1[@class='title']//text()").extract_first("未知")
        item['news_pub_time'] = response.xpath("//span[@class='time']//text()").extract_first("未知")
        item["news_url"] = response.url
        item["update_time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        yield item
        

        # 存储网页源码
        news_source_code = "<meta charset='utf8'> \n" + re.sub('src="/','src="{0}/'.format(domain),response.xpath("//div[@class='right_list wenzhang_contain_1']").extract_first())
        dir_path = "source_pages//" + self.name # 文件夹路径
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
        date = time.strftime("%Y-%m-%d", time.localtime())
        try:
            file_path = dir_path + "//" + date + "_" +md5(news_source_code.encode("utf-8")).hexdigest() + ".html"
        except:
            file_path = dir_path + "//" + date + "_" +md5((news_source_code+str(random.randint(1,10000))).encode("utf-8")).hexdigest() + ".html"
        with open(file_path,"w",encoding="utf-8") as f:
            f.write(news_source_code)

    
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
            # print("***tesing***:" + str(len(xwdt_news_url_list))+str(len(tzgg_news_url_list))+str(len(bfxx_news_url_list))+str(len(qtgs_news_url_list))+str(len(syjx_news_url_list)))
            yield scrapy.Request(news_url, self.parse)