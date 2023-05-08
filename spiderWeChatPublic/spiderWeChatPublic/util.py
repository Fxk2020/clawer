# -*- encoding: utf-8 -*-
'''
@File    :   util.py   
@Contact :   13105350231@163.com
@License :   (C)Copyright 2022-2025
@Desciption : 工具类


@Modify Time      @Author    @Version   
------------      -------    --------   
2023/5/6 14:23   fxk        1.0         
'''
import pymysql
from selenium import webdriver
from spiderWeChatPublic.settings import WEBDRIVER_PATH
import pdfkit
import datetime
import wechatsogou
import multiprocessing
import time
from spiderWeChatPublic.settings import *

ws_api = wechatsogou.WechatSogouAPI(captcha_break_time=3)

JS_DropDownScript = """
    (function () {
    var y = 0;
    var step = 100;
    window.scroll(0, 0);
    function f() {
    if (y < document.body.scrollHeight) {
    y += step;
    window.scroll(0, y);
    setTimeout(f, 100);
    } else {
    window.scroll(0, 0);
    document.title += "scroll-done";
    }
    }
    setTimeout(f, 1000);
    })();
    """


def create_chrome_driver(*, headless=False):
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument('--headless')
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    browser = webdriver.Chrome(options=options,
                               executable_path=WEBDRIVER_PATH)
    browser.execute_cdp_cmd(
        'Page.addScriptToEvaluateOnNewDocument',
        {'source': 'Object.defineProperty(navigator,"webdriver",{get: () => undefined}'}
    )
    return browser


def drop_down(browser):
    browser.execute_script(JS_DropDownScript)
    print("下拉中...")
    # 阻塞住这个方法，显示全部源代码
    while True:
        if "scroll-done" in browser.title:
            return browser.page_source


def url2pdf(item):
    '''
    使用pdfkit生成pdf文件
    :param url: 文章url
    :param title: 文章标题
    :param targetPath: 存储pdf文件的路径
    '''
    url = item[1]
    title = item[0]
    targetPath = PDF_SAVE_URL+"{}.pdf".format(item[0])
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
        print(title + "ok")
    except:
        # 部分文章标题含特殊字符，不能作为文件名
        filename = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.pdf'
        pdfkit.from_string(html, PDF_SAVE_URL + filename, configuration=config)


def selectDbItems():
    # 打开数据库连接
    db = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_DATABASE,
                         charset='utf8')

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    # SQL 插入语句
    sql = "select * from "+TABLE_NAME
    # print(sql)
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
        items = cursor.fetchall()
    except pymysql.Error:
        # Rollback in case there is any error
        print(pymysql.Error)
        print(sql)
        db.rollback()
        items = None
    # 关闭数据库连接
    db.close()
    return items


def getPdfs():
    items = selectDbItems()
    print(items)
    start = time.time()
    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    pool.map(url2pdf, items)
    pool.close()
    pool.join()
    end = time.time()

    print(end - start)

def readAlbumIds(url='C:\\Users\\yuanbao\\Desktop\\myGitHub\\clawer\\spiderWeChatPublic\\spiderWeChatPublic\\album_ids'):
    result = []
    with open(url, 'r', encoding='utf-8') as f:
        for line in f:
            result.append(line.strip('\n'))
    return result


if __name__ == '__main__':
    # result = readAlbumIds("C:\\Users\\yuanbao\\Desktop\\myGitHub\\clawer\\spiderWeChatPublic\\spiderWeChatPublic\\album_ids")
    # print(result)
    # print(result[11:])
    getPdfs()