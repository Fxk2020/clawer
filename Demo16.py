# -*- encoding: utf-8 -*-
'''
@File    :   Demo16.py   
@Contact :   13105350231@163.com
@License :   (C)Copyright 2022-2025
@Desciption : 测试fiddler进行手机抓包--爬取微信公众号的文章，存到数据库中并下载为pdf(第一版)

@Modify Time      @Author    @Version   
------------      -------    --------   
2023/4/3 20:27   fxk        1.0         
'''
import json
import time

import MySQLdb
import requests

base_url = 'https://mp.weixin.qq.com/mp/homepage'
# base_url = "https://mp.weixin.qq.com/mp/homepage"
headers = {
    "Connection": "keep-alive",
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Linux; Android 13; M2102K1AC Build/TKQ1.220829.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/107.0.5304.141 Mobile Safari/537.36 XWEB/5023 MMWEBSDK/20230202 MMWEBID/752 MicroMessenger/8.0.33.2320(0x28002151) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
    "Referer": "https://mp.weixin.qq.com/mp/homepage?__biz=MzUyMzUyNzM4Ng==&hid=2&sn=843f5f669417669e281b37438aa38b03&scene=18&devicetype=android-33&version=28002151&lang=zh_CN&nettype=WIFI&ascene=7&session_us=gh_6c6111156d8c&pass_ticket=m51mP9Xjz3mIHgQQP%2BJ3cp5vcNFZxwQAvYx%2FRRPrlqIR%2Buh%2BLv93FA7EPi7GRwVn0vD5GBQ5a8ogZuP6RSpL8w%3D%3D&wx_header=3",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
}

cookies = {
    "wxuin": "1206466542",
    "devicetype": "android-33",
    "version": "28002151",
    "lang": "zh_CN",
    "appmsg_token": "1211_Rsr5atSNq4vCvK8NIeypgzfzRnNiTqX455I6R5QZpF-sS2iMg2Mby9rUkWCiL8fBblJ16I0qZ8uTOdHD",
    "rewardsn": "",
    "wxtokenkey": "777",
    "pass_ticket": "m51mP9Xjz3mIHgQQP+J3cp5vcNFZxwQAvYx/RRPrlqIR+uh+Lv93FA7EPi7GRwVn0vD5GBQ5a8ogZuP6RSpL8w::",
    "wap_sid2": "CO7vpL8EEooBeV9ISmZwQ3k0QTdmNHpZMDU4NHVOekdnU09Sby0zcUFDdGh4NTQ3YmNkRE1fWlBKNzRvejZFb19tWG5MX3lyVDU5N0xNN2JjZEdDaGk1SW9ncTlpb0hHZ0RKYkJDSzg5bENTSzBRSnBaYk45blpzWE9HQVBWemlWRW5oeHN0cGZhVU9wa1NBQUF+MLeoq6EGOAxAlE4:"
}


def insertDbItems(title, cover, link):
    # 打开数据库连接
    db = MySQLdb.connect("rm-2zes1vjbzf4mv635rdo.mysql.rds.aliyuncs.com", "fxk", "Fxk199959", "TestCrawl",
                         charset='utf8')

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    # SQL 插入语句
    sql = "INSERT INTO xiaoli VALUES ('" + title + "','" + \
          cover + "','" + link + "')"
    # print(sql)
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except MySQLdb.Error:
        # Rollback in case there is any error
        print(MySQLdb.Error)
        print(sql)
        db.rollback()

    # 关闭数据库连接
    db.close()


def selectDbItems():
    # 打开数据库连接
    db = MySQLdb.connect("rm-2zes1vjbzf4mv635rdo.mysql.rds.aliyuncs.com", "fxk", "Fxk199959", "TestCrawl",
                         charset='utf8')

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    # SQL 插入语句
    sql = "select * from xiaoli"
    # print(sql)
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
        items = cursor.fetchall()
    except MySQLdb.Error:
        # Rollback in case there is any error
        print(MySQLdb.Error)
        print(sql)
        db.rollback()
        items = None
    # 关闭数据库连接
    db.close()
    return items


def get_params(hid, begin, count):
    params = {
        "__biz": "MzUyMzUyNzM4Ng==",
        "hid": "{}".format(hid),
        "sn": "843f5f669417669e281b37438aa38b03",
        "scene": "18",
        "devicetype": "android-33",
        "version": "28002151",
        "lang": "zh_CN",
        "nettype": "WIFI",
        "ascene": "7",
        "session_us": "gh_6c6111156d8c",
        "pass_ticket": "+HAP3q4K/58MUV3LqRV4jatlxOfkeAhkfn5GeDeCFSKhme8iAGC9tJ/muNEUIiCkEbg+GNFaZ3WFM9Lq9pF27Q==",
        "wx_header": "3",
        "begin": "{}".format(begin),
        "count": "{}".format(count),
        "action": "appmsg_list",
        "f": "json",
        "r": "0.1276703516879698",
        "appmsg_token": "1211_pAPHUVlZq+emVHnF6j4w2fll6dxIHIBtPPovTQ~~"
    }
    return params


def get_list_data(hid, begin, count):
    res_json = requests.post(base_url, headers=headers, params=get_params(hid, begin, count), cookies=cookies)
    # print(res_json.text)
    date = json.loads(res_json.text)
    articles = date['appmsg_list']
    number = 0
    for article in articles:
        print("文章的标题是：%s,图片连接是%s,文章连接是%s" % (article['title'], article['cover'], article['link']))
        # 插入到数据库
        insertDbItems(article['title'], article['cover'], article['link'])
        number = number + 1
    return number


def get_little_articles():
    hids = [2, 3, 5, 6, 7, 8]
    max_count = 100
    start_page = 0
    amount = 0
    for hid in hids:
        temp = get_list_data(hid, start_page, max_count)
        amount = amount + temp
    print(amount)


if __name__ == '__main__':
    items = selectDbItems()
    for item in items:
        print(item[0])
        print(item[2])
        print("===========================")
    # get_little_articles()
