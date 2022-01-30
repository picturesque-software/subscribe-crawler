import os
import time

# 定时执行

while True:
    time_now = time.strftime("%H:%M", time.localtime())  # 刷新
    if time_now == "7:30" or time_now == "11:30" or time_now == "20:34":  # 此处设置每天定时的时间
        os.system("scrapy crawl sbc_spider")  # 爬取实验设备管理处
        os.system("scrapy crawl jw_spider")  # 爬取本科生院
        time.sleep(14400)  # 每隔4h运行一次