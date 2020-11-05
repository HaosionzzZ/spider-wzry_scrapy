import scrapy
import json
from selenium import webdriver
from scrapy.http import HtmlResponse
from scrapy.selector import Selector
import re
from time import sleep
import random


class HeroSpider(scrapy.Spider):
    name = 'hero'
    allowed_domains = ['pvp.qq.com']
    start_urls = ['https://pvp.qq.com/web201605/js/herolist.json']

    # def __init__(self):
    #     self.browser=webdriver.Chrome(executable_path="C:\PythonTools\Chrome\chromedriver.exe")

# 访问数据源地址获取到保存所有英雄信息的json文件
    def parse(self, response):
        datas = json.loads(response.body_as_unicode())
        for data in datas:
            item = {}
            item["hero_name"] = data["cname"]
            item["hero_title"] = data["title"]
            item["hero_href"] = "https://pvp.qq.com/web201605/herodetail/"+str(data["ename"])+".shtml"
            driver = webdriver.Chrome(executable_path="C:\PythonTools\Chrome\chromedriver.exe")
            driver.get(item["hero_href"])
            new_response = HtmlResponse(url=response.url, body=driver.page_source, encoding='utf-8')
            skin_li = new_response.xpath("//div[@class='pic-pf']/ul[@class='pic-pf-list pic-pf-list3']/li").extract()
            # print(skin_li)
            skin_list = []
            # 注意此处的skin为字符串类型
            for skin in skin_li:
                # print(skin)
                # print("skin的类型是{}".format(type(skin)))
                # skin=Selector(text=skin)
                # print(skin)
                skin_dict = {}
                # 使用正则表达式获取指定位置的字符串
                skin_name = re.findall(r'data-title="(.*)" data-icon', skin)
                skin_img = re.findall(r'data-imgname="(.*)" data-title', skin)
                skin_dict["skin_name"]=skin_name[0]
                skin_dict["skin_img"]="https:"+str(skin_img[0])
                # skin_dict["skin_name"] = skin.xpath("li/i/img/@data-title").extract_first()
                # skin_dict["skin_img"] = "https:" + str(skin.xpath("li/i/img/@data-imgname").extract_first())
                skin_list.append(skin_dict)
            item["skin_list"] = str(skin_list)
            sleep_time = random.randint(1,3)
            sleep(sleep_time)
            driver.quit()
            yield item
            # yield scrapy.Request(
            #     item["hero_href"],
            #     callback=self.hero_detail,
            #     meta={"item": item}
            # )

# 进入英雄详情页获取信息
#     def hero_detail(self, response):
#         skin_li=response.xpath("//div[@class='pic-pf']/ul[@class='pic-pf-list pic-pf-list3']/li").extract()
#         item = response.meta["item"]
#         skin_list = []
#         for skin in skin_li:
#             skin_dict = {}
#             skin_dict["skin_name"]=skin.xpath("./i/img/@data-title").extract_first()
#             skin_dict["skin_img"]="https:"+skin.xpath("./i/img/@data-imgname").extract_first()
#             skin_list.append(skin_dict)
#         item["skin_list"]=skin_list
#         yield item

    # def closed(self, spider):
    #     print("closed")
    #     self.browser.quit()
