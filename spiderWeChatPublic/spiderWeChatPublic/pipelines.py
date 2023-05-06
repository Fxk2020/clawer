# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymysql
from itemadapter import ItemAdapter
from spiderWeChatPublic.settings import *

class SpiderwechatpublicPipeline:
    def __init__(self):
        self.conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_DATABASE,
                                    charset=DB_CHARSET)
        self.cursor = self.conn.cursor()
        self.data = []

    def close_spider(self, spider):
        """
                关闭爬虫，回调
                :param spider:
                :return:
        """
        # self.conn.commit()
        if len(self.data) > 0:
            self.insertMany()
        self.conn.close()

    def open_spider(self, spider):
        """
        打开爬虫，回调
        :param spider:
        :return:
        """
        pass

    def process_item(self, item, spider):
        """
        爬取到数据，回调（多次）
        :param item:
        :param spider:
        :return:
        """
        article_title = item.get('article_title')
        article_link = item.get('article_link')
        article_time = item.get('article_time')
        image_link = item.get('image_link')

        self.data.append((article_title, article_link, article_time, image_link))
        if len(self.data) == 50:
            self.insertMany()
        return item

    def insertMany(self):
        # print('insert into `taobao` VALUES (%s, %s, %s, %s, %s, %s)', self.data)
        self.cursor.executemany('insert into `wechatpublic` VALUES (%s, %s, %s, %s)', self.data)
        self.conn.commit()
        self.data.clear()
