# 爬取微信公众号--渤海小吏的文章

## 一、目的

最近在读一个微信公众号渤海小吏的文章，非常喜欢这里面的文章，想着如果能把这里面的文章爬取下来保存就好了。

正好这学期要学习信息检索这门课，于是打算爬取公众号上的文章。

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

查看文章发现存在几篇文章并未下载的问题，查看日志：

![image-20230405201348895](https://oss-img-fxk.oss-cn-beijing.aliyuncs.com/markdown/image-20230405201348895.png)

![image-20230405201443001](https://oss-img-fxk.oss-cn-beijing.aliyuncs.com/markdown/image-20230405201443001.png)

打开对映网址，发现文章存在违规，已经下架了：

![image-20230405201513184](https://oss-img-fxk.oss-cn-beijing.aliyuncs.com/markdown/image-20230405201513184.png)

ok，所有合规的文章已经全部爬取下来了，查看文章

![image-20230405201553619](https://oss-img-fxk.oss-cn-beijing.aliyuncs.com/markdown/image-20230405201553619.png)

yes舒服了。这下不怕没有文章看了，哈哈哈。

## 四、源代码

----test.html和test2.html是爬取的无图片的网页

----Demo16用于爬取有图片的文章

----Demo17用于爬取无图片的文章

-----Demo18用于将网页HTML转换为文章PDF

