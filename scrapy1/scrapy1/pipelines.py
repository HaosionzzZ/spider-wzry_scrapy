# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql


class Scrapy1Pipeline:
    def __init__(self):
        # 连接MySQL数据库
        self.connect=pymysql.connect(host='localhost', user='root', password='zhong123456789', db='wzry', port=3306)
        self.cursor=self.connect.cursor()
        self.cursor.execute('delete from hero_inf')

    def process_item(self, item, spider):
        # 往数据库里面写入数据
        skin_count = pymysql.escape_string(item['skin_list'])
        self.cursor.execute(
            'insert into hero_inf(hero_title,hero_name,hero_href,skin_list)VALUES ("{}","{}","{}","{}")'.format(
                item['hero_title'], item['hero_name'], item['hero_href'], skin_count))
        self.connect.commit()
        print(item)
        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.connect.close()
