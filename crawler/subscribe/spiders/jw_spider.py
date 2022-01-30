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


class JwSpiderSpider(scrapy.Spider):
    name = 'jw_spider'
    allowed_domains = ['jw.nju.edu.cn']
    start_urls = ['https://jw.nju.edu.cn/13/3b/c24774a529211/page.htm']

    def parse(self, response):
        
        item = SubscribeItem()
        item['web_name'] = "jw"
        item['news_author'] = response.xpath("//span[@class='arti_publisher']//text()").extract_first("本科生院")
        news_title= response.xpath("//h1[@class='arti_title']//text()").extract_first("")
        if len(news_title) <=0:
            news_title = response.xpath("//title//text()").extract_first("未知")

        domain = parse.urlparse(response.url).scheme + "://" + parse.urlparse(response.url).netloc
        item['news_source_code'] = "<meta charset='utf8'> \n" + re.sub('src="/','src="{0}/'.format(domain),response.xpath("//div[@id='d-container']").extract_first())
        item['news_title'] = news_title
        item['news_pub_time'] = response.xpath("//span[@class='arti_update']//text()").extract_first("未知")
        item["news_url"] = response.url
        item["news_visit"] = response.xpath("//span[@class='WP_VisitCount']//text()").extract_first("未知")
        item["update_time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # item['news_cat'] = '' # 暂不分类
        yield item

        # 存储网页源码
        news_source_code = "<meta charset='utf8'> \n" + re.sub('src="/','src="{0}/'.format(domain),response.xpath("//div[@id='d-container']").extract_first())
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
        # 公告通知
        announcement_url = "https://jw.nju.edu.cn/ggtz/list1.htm"
        # 教学动态
        teaching_url = "https://jw.nju.edu.cn/_s414/24774/list1.psp"
        announcement_soup = get_response(announcement_url)
        teaching_soup = get_response(teaching_url)
        announcement_url_news_list = [i.a["href"] for i in announcement_soup.find_all(class_="news_title")]
        teaching_url_news_list = [i.a["href"] for i in teaching_soup.find_all(class_="news_title")]
        base_url = "https://jw.nju.edu.cn/"
        for url in announcement_url_news_list + teaching_url_news_list:
            if not url.startswith("http"):
                news_url = base_url + url
            else:
                news_url = url
            yield scrapy.Request(news_url, self.parse)


