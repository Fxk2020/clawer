# 爬取微信公众号专辑文章

## 一、目的

最近在读一个微信公众号渤海小吏的文章，非常喜欢这里面的文章，想着如果能把这里面的文章爬取下来保存就好了。

正好这学期要学习信息检索这门课，于是打算爬取该微信公众号上的所有文章进行下载。

## 二、用到的包和框架

python中主要用到这几个包

```python
request
json
BeautifulSoup
MySQLdb
pdfkit
```

使用抓取手机包的工具：

```python
Fiddler4
```

发现一个神器可以将爬取文章网页转变为pdf：

```python
wechatsogou
```

##  三、爬取的过程

总体思路：

- 我们通过 [fiddler](http://telerikchina.com/files/FiddlerSetup.exe) 来抓取手机上的请求,	分析请求获得文章的url和请求参数
- 将公众号历史文章的url等关键信息爬取下来存到数据库中
- 最后使用pdfkit制作成 pdf 文件，报错到磁盘上

思路答题如下，小帅b代表的就是用户：

![图片](https://mmbiz.qpic.cn/mmbiz_png/J2icnQspGlaLAcBLmgMAiaZqPXa2DZ7GD9ImSPIibghvZo5wenlTe9HfwwURszEF1MlLqTKoYBnjicUPMT9C3S7Axg/640?wx_fmt=png&wxfrom=5&wx_lazy=1&wx_co=1)

### 3.1 爬取手机的请求获得url和请求参数

#### 3.1.1 fiddler抓取手机请求

fiddler可以帮助我们抓取浏览器的请求：

从下图

![图片](https://mmbiz.qpic.cn/mmbiz_png/J2icnQspGlaId8PzOrFwXBYAALugG4iaa3KTZzMMickqhasJHfKTYJLavtgfiaTgYXKUlGkjFfrjaUZZjNqFziak2ibA/640?wx_fmt=png&wxfrom=5&wx_lazy=1&wx_co=1)

变为：

![图片](https://mmbiz.qpic.cn/mmbiz_png/J2icnQspGlaId8PzOrFwXBYAALugG4iaa3u6LXu5gfEcMFw2TMqx60ia1GFgNDeaxFVqDHkjgq4Tevd4qWAic1r0Mg/640?wx_fmt=png&wxfrom=5&wx_lazy=1&wx_co=1)

安装fiddler，下载证书，在浏览器输入localhost:8888，出现如下界面：

![image-20230405193146873](https://oss-img-fxk.oss-cn-beijing.aliyuncs.com/markdown/image-20230405193146873.png)

说明安装成功。

接下来配置手机使用 Fiddler 来抓取我们手机上的数据：

![image-20230406104918647](https://oss-img-fxk.oss-cn-beijing.aliyuncs.com/markdown/image-20230406104918647.png)

选择如上设置。然后使电脑和手机处于同一ip地址下（校园网sdu不行，可以使用实验室局域网或者是自己的热点）。

查看电脑ip地址，在手机上打开连接的wifi，输入代理服务器和端口--服务器就是自己电脑的IP地址，端口是8888.

![image-20230406104929175](https://oss-img-fxk.oss-cn-beijing.aliyuncs.com/markdown/image-20230406104929175.png)

紧接着手机打开浏览器输入你的 IP地址和端口，下载安装证书。

![image-20230406104939859](https://oss-img-fxk.oss-cn-beijing.aliyuncs.com/markdown/image-20230406104939859.png)

然后小米手机在设置中进行安装。然后打开电脑上的fiddler可以看到，可以抓到手机上的请求。打开qq可以看到如下请求

![image-20230406104946777](https://oss-img-fxk.oss-cn-beijing.aliyuncs.com/markdown/image-20230406104946777.png)

最大的返回是英雄杀的广告，不愧是你腾讯。

接下来打开微信公众号，进入历史文章，可以看到有两类：

- 有图片的

![image-20230405194601658](https://oss-img-fxk.oss-cn-beijing.aliyuncs.com/markdown/image-20230405194601658.png)

- 无图片的

![image-20230405194612709](https://oss-img-fxk.oss-cn-beijing.aliyuncs.com/markdown/image-20230405194612709.png)

肯定要分两类进行爬取。

#### 3.1.2 查找并分析请求

- 有图片的简单

  直接返回了json数据，直接提取文章题目，图片地址和文章地址

  ![image-20230405194914079](https://oss-img-fxk.oss-cn-beijing.aliyuncs.com/markdown/image-20230405194914079.png)

  查看请求头和请求参数：

  ![image-20230405195032043](https://oss-img-fxk.oss-cn-beijing.aliyuncs.com/markdown/image-20230405195032043.png)

  注意该请求是post请求！！！！

  最重要的是begin和count这两个参数：

  ![image-20230405195335921](https://oss-img-fxk.oss-cn-beijing.aliyuncs.com/markdown/image-20230405195335921.png)

  一个表示从那篇文章开始，一个表示共显示几篇文章。我们可以控制这两个参数来爬取文章。

- 无图片的复杂一点

  - 返回的是html--需要使用beautifulsoup进行分析。

    ![image-20230405195544517](https://oss-img-fxk.oss-cn-beijing.aliyuncs.com/markdown/image-20230405195544517.png)

  - 请求参数--

    ![image-20230405195705367](https://oss-img-fxk.oss-cn-beijing.aliyuncs.com/markdown/image-20230405195705367.png)

    - mid--不同专栏不同的数字
    - idx--应该是腾讯内部进行计数的
    - chksm，exportkey，sn，pass_ticket都需要控制否则会产生参数错误。

  - 对网页进行分析：

    - 具体内容

      ![image-20230405195912403](https://oss-img-fxk.oss-cn-beijing.aliyuncs.com/markdown/image-20230405195912403.png)

    - 文章名，文章url都是集中在这个div下，通过beautifulsoup获得进行爬取。



### 3.2 将爬取的内容存到数据库中

通过python，将爬取的文章题目，图片地址（无图片的插入无图片），文章链接存到mysql数据库中。

![image-20230405200049571](https://oss-img-fxk.oss-cn-beijing.aliyuncs.com/markdown/image-20230405200049571.png)

![image-20230405200142211](https://oss-img-fxk.oss-cn-beijing.aliyuncs.com/markdown/image-20230405200142211.png)

共爬取了586篇文章。

### 3.3 通过pdfkit将文章转为pdf

使用wechatsogou和pdfkit两个包将网页html代码直接转变为pdf文章，并保存到磁盘上。

使用wechatsougo的错误--

![image-20230506170049512](https://oss-img-fxk.oss-cn-beijing.aliyuncs.com/markdown/image-20230506170049512.png)

[解决方案](https://github.com/Azure-Samples/ms-identity-python-webapp/issues/16)

查看文章发现存在几篇文章并未下载的问题，查看日志：

![image-20230405201348895](https://oss-img-fxk.oss-cn-beijing.aliyuncs.com/markdown/image-20230405201348895.png)

![image-20230405201443001](https://oss-img-fxk.oss-cn-beijing.aliyuncs.com/markdown/image-20230405201443001.png)

打开对映网址，发现文章存在违规，已经下架了：

![image-20230405201513184](https://oss-img-fxk.oss-cn-beijing.aliyuncs.com/markdown/image-20230405201513184.png)

ok，所有合规的文章已经全部爬取下来了，查看文章

![image-20230405201553619](https://oss-img-fxk.oss-cn-beijing.aliyuncs.com/markdown/image-20230405201553619.png)

有的图片也可以正常显示：

![image-20230425151434415](https://oss-img-fxk.oss-cn-beijing.aliyuncs.com/markdown/image-20230425151434415.png)

yes舒服了。这下不怕没有文章看了，哈哈哈。

--------------------------------------------------------------

2023.5.6更新，手机获取专辑号，scrapy配合selenium自动化爬取+下载（完美版，所有文章都有图片）

## 四 项目重构

之前是完全自己手写的代码实现，后来在学习爬取淘宝信息的时候学到了scrapy框架。如获至宝，可以省去很多自己手写的代码，而且健壮性和易读性都比我自己写的代码要好很多，于是就对我之前的代码进行了重构。

而且这次的思路也和之前略有不同，经过观察发现该公众好的文章都放到了专辑中（专辑是微信对于公众号管理退出的一种管理方式）。发现通过专辑号可以在电脑端访问所有专辑下的文章，于是就可以从手机获取所有专辑的专辑号，然后在电脑端进行自动爬取下载。

以山东大学的一些专辑为例，滑动到页面最后，展示所有文章后，对文章进行爬取。

![image-20230521164113825](https://oss-img-fxk.oss-cn-beijing.aliyuncs.com/markdown/image-20230521164113825.png)

### 4.1使用scrapy对项目进行重构

```python
Scrapy==2.8.0
selenium==3.141.0
```

- 使用fiddler从手机获取每个公众号专辑的id，并记录到album_ids中

  ```
  #起始网址
  start_url = "https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MzUyMzUyNzM4Ng==&action=getalbum&album_id="
  
  # 按照渤海小吏的专辑次序排列
  album_ids = [
      '1339909853384622082',
      '1339904567118741505',
      '1339922909934206977',
      '1339936409721061378',
      '1339959586404777985',
      '1339972960463175682',
      '1622271317351727106',
      '2091728990028824579',
      '2790568009419210757']
  ```

- 在item中，需要爬取的是文章的题目、地址、发布时间和文章图片的地址

  ```python
  article_title = scrapy.Field()
  article_link = scrapy.Field()
  article_time = scrapy.Field()
  image_link = scrapy.Field()
  ```

- 在pipelines中，配置链接数据库并将爬取的数据输出到数据库中保存

- 在DownloaderMiddleware中，使用selenium打开网址，并进行动态加载（滑动到最底端，才能展示出专辑下的所有文章），并返回网页源代码。

- util中封装了创建selenium驱动，向下滑动页面，将页面转换为pdf的方法

- 爬虫使用BeautifulSoup对DownloaderMiddleware返回的网页源代码进行解析，返回每一项内容

- 在setting中进行自己电脑的配置

  ```
  # selenium中webdriver的地址
  WEBDRIVER_PATH = ''
  # 数据库的相关配置
  DB_HOST = ""
  DB_USER = ""
  DB_PASSWORD = ""
  DB_DATABASE = ""
  DB_CHARSET = "utf-8"
  ```

- 开启爬取

  ```
   scrapy crawl wechatPublic
  ```

  

### 4.2 结果

数据库结构：

![image-20230506212717241](https://oss-img-fxk.oss-cn-beijing.aliyuncs.com/markdown/image-20230506212717241.png)

下载的公众号文章

![image-20230506212958869](https://oss-img-fxk.oss-cn-beijing.aliyuncs.com/markdown/image-20230506212958869.png)

![image-20230506213032730](https://oss-img-fxk.oss-cn-beijing.aliyuncs.com/markdown/image-20230506213032730.png)

ok完美了

### 4.3 拓展

发现不光可以爬取渤海小吏的文章，只要是微信公众号的专辑都可以爬取.

爬取步骤如下

#### 4.3.1 获取文章专辑号

从手机获取文章的专辑号：

- 找到请求url![image-20230508102037651](https://oss-img-fxk.oss-cn-beijing.aliyuncs.com/markdown/image-20230508102037651.png)

- 找到对映的专辑号

  ![image-20230508102101404](https://oss-img-fxk.oss-cn-beijing.aliyuncs.com/markdown/image-20230508102101404.png)

![](https://oss-img-fxk.oss-cn-beijing.aliyuncs.com/markdown/image-20230508101554948.png)

#### 4.3.2 更改数据库相关设置，修改表名

#### 4.3.3 获取专辑号进行爬取

```
def readAlbumIds(url='C:\\Users\\yuanbao\\Desktop\\myGitHub\\clawer\\spiderWeChatPublic\\spiderWeChatPublic\\album_ids'):
    result = []
    with open(url, 'r', encoding='utf-8') as f:
        for line in f:
            result.append(line.strip('\n'))
    return result
```

```
# 按照渤海小吏的专辑次序排列
all_album_ids = readAlbumIds()
album_ids = all_album_ids[16:]
```

#### 4.3.4 进行下载

```
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
```

## 五、源代码

已经将源代码放到了GitHub上，地址：https://github.com/Fxk2020/clawer

- test.html和test2.html是爬取的无图片的网页

- Demo16用于爬取有图片的文章

- Demo17用于爬取无图片的文章

- Demo18用于将网页HTML转换为文章PDF

- 需要的类包和对应版本放到requestments.txt中了

  ---------------------------------------------------------------------------------

- 重构的项目放到了spiderWeChatPublic文件夹下

