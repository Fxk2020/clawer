# -*- encoding: utf-8 -*-
'''
@File    :   Demo18.py
@Contact :   13105350231@163.com
@License :   (C)Copyright 2022-2025
@Desciption : 提取数据库的文章地址下载成pdf

@Modify Time      @Author    @Version
------------      -------    --------
2023/4/4 16:41   fxk        1.0
'''
import os
import time

import pdfkit
import datetime
import wechatsogou
import multiprocessing
import time
# 初始化API
from Demo16 import selectDbItems

ws_api = wechatsogou.WechatSogouAPI(captcha_break_time=3)


def url2pdf(item):
    '''
    使用pdfkit生成pdf文件
    :param url: 文章url
    :param title: 文章标题
    :param targetPath: 存储pdf文件的路径
    '''
    url = item[2]
    title = item[0]
    targetPath = "D:\\xiaoli\\{}.pdf".format(item[0])
    try:
        content_info = ws_api.get_article_content(url)
        print("ok")
    except:
        print(url)
        print("false")
        return False
    # 处理后的html
    html = f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>{title}</title>
    </head>
    <body>
    <h2 style="text-align: center;font-weight: 400;">{title}</h2>
    {content_info['content_html']}
    </body>
    </html>
    '''
    try:
        # path_wk = "E:/softwareAPP/wkhtmltopdf/bin/wkhtmltopdf.exe";
        config = pdfkit.configuration()
        pdfkit.from_string(input=html, output_path=targetPath, configuration=config)
        print(title+"ok")
    except:
        # 部分文章标题含特殊字符，不能作为文件名
        filename = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.pdf'
        pdfkit.from_string(html, "D:\\xiaoli\\"+filename, configuration=config)


if __name__ == '__main__':
    items = selectDbItems()
    start = time.time()
    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    pool.map(url2pdf, items)
    pool.close()
    pool.join()
    end = time.time()

    print(end - start)



