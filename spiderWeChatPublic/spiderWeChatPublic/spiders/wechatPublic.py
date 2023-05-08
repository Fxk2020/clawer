import re

import scrapy
from bs4 import BeautifulSoup
from spiderWeChatPublic import util

from spiderWeChatPublic.items import Article
from spiderWeChatPublic.util import readAlbumIds


class WechatpublicSpider(scrapy.Spider):
    name = "wechatPublic"
    allowed_domains = ["mp.weixin.qq.com"]
    start_url = "https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MzUyMzUyNzM4Ng==&action=getalbum&album_id="

    def start_requests(self):
        # 按照渤海小吏的专辑次序排列
        all_album_ids = readAlbumIds()
        album_ids = all_album_ids[23:]
        for album_id in album_ids:
            yield scrapy.Request(self.start_url + "" + album_id)

    def parse(self, response):
        # print(response.text)
        soup = BeautifulSoup(response.text, "lxml")
        articles = soup.findAll('li')
        for article in articles:
            item = Article()
            item['article_title'] = article.get('data-title')
            item['article_link'] = article.get('data-link')
            if article.find('span', class_='js_article_create_time album__item-info-item') is not None:
                item['article_time'] = article.find('span', class_='js_article_create_time album__item-info-item').text
            if article.find('div', class_="album__item-img") is not None:
                if article.find('div', class_="album__item-img").get('style') is not None:
                    item['image_link'] = article.find('div', class_="album__item-img").get('style').split("url")[
                        1].replace('(', "").replace(')', "")
            if item.get('article_title') is not None:
                yield item
