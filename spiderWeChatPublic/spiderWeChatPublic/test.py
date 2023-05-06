# -*- encoding: utf-8 -*-
'''
@File    :   test.py   
@Contact :   13105350231@163.com
@License :   (C)Copyright 2022-2025
@Desciption : -----------------------------------
selenium 下拉到页面最底端
https://blog.51cto.com/u_15067237/4225407

@Modify Time      @Author    @Version   
------------      -------    --------   
2023/5/6 14:47   fxk        1.0         
'''
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re

from bs4 import BeautifulSoup
from selenium import webdriver
import time

import spiderWeChatPublic.settings
from spiderWeChatPublic import util

def test1():
    url = "https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MzUyMzUyNzM4Ng==&action=getalbum&album_id=2091728990028824579&scene=126&devicetype=android-33&version=2800233d&lang=zh_CN&nettype=WIFI&ascene=3&pass_ticket=ndohy9BRu98hNGwsP7av4bI%2FNEicC%2Bp2IuZXRmI4CWeEhehaoa68t%2F8IXvQfw9LF%2BQfqUNLftc0%2FFJvF5FUuqA%3D%3D&wx_header=3"

    browser = webdriver.Chrome(executable_path=spiderWeChatPublic.settings.WEBDRIVER_PATH)
    browser.get(url)

    browser.execute_script(util.JS_DropDownScript)
    print("下拉中...")
    # time.sleep(180)
    while True:
        if "scroll-done" in browser.title:
            break
    else:
        print("还没有拉到最底端...")
        time.sleep(3)

if __name__ == '__main__':
    # 下载下来的网页源代码
    f = open("C:\\Users\\yuanbao\\Desktop\\myGitHub\\clawer\\spiderWeChatPublic\\1.html", encoding='utf-8')
    lines = f.read()
    # print(lines)
    f.close()
    soup = BeautifulSoup(lines, "lxml")
    articles = soup.findAll('li')
    i=1
    for article in articles:

        print(article.get('data-title'))
        print(article.get('data-link'))
        if article.find('span', class_='js_article_create_time album__item-info-item') is not None:
            print(article.find('span', class_='js_article_create_time album__item-info-item').text)
        if article.find('div', class_="album__item-img") is not None:
            if article.find('div', class_="album__item-img").get('style') is not None:
                print(article.find('div', class_="album__item-img").get('style').split("url")[1].replace('(', "").replace(')', ""))
        print(i)
        i = i+1
