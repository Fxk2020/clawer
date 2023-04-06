# -*- encoding: utf-8 -*-
'''
@File    :   Demo17.py   
@Contact :   13105350231@163.com
@License :   (C)Copyright 2022-2025
@Desciption : 测试fiddler进行手机抓包--爬取微信公众号的文章，存到数据库中并下载为pdf(第一版)

@Modify Time      @Author    @Version   
------------      -------    --------   
2023/4/4 15:04   fxk        1.0         
'''
import requests
from bs4 import BeautifulSoup
from Demo16 import insertDbItems

# https://mp.weixin.qq.com/s?__biz=MzUyMzUyNzM4Ng==&mid=100001858&idx=1&sn=bd7345366a61a46d30d1aa85d63e2ab0&chksm=7a3a7df74d4df4e12a162f7a04ee5182154d009ff3fa4bb0e81155e1b3d1720851f8d07635e6&scene=18&ascene=7&devicetype=android-33&version=28002151&nettype=WIFI&abtest_cookie=AAACAA%3D%3D&lang=zh_CN&session_us=gh_6c6111156d8c&countrycode=CN&exportkey=n_ChQIAhIQrmC0P%2BEVy4w8YfzsS4sN1hLrAQIE97dBBAEAAAAAAGptFb7Eku8AAAAOpnltbLcz9gKNyK89dVj079xPHweohHib6dXGmlSiZApT%2FlH3RQTlTXYma7hdzTsM6tL0UyFb%2Fe70%2BPn8QrSRgJCzNXvByvnXm7w6D8eeqbNXVX92VkEj4E39yOWnT9fpIxnuanV9feTtI07VqrDAlc3uIz9kMJj3FeIQUnNIFaDcx548oWPqvvAbrvJLV8JJdN%2Bytw6wx81yMSFdT8LW8BOEFJYQbcdAp27%2FtGeq9i2r4PsXxh1Sn609mIhnJmZYhrvoRMlI9oSEETLsKceNHJZm07g%3D&pass_ticket=%2BHAP3q4K%2F58MUV3LqRV4jatlxOfkeAhkfn5GeDeCFSLanu7kv%2FMsRzJlbfh1cTG2b7NlungmQSbfm3TBnX4e%2BA%3D%3D&wx_header=3
base_url = 'https://mp.weixin.qq.com/s'
# base_url = "https://mp.weixin.qq.com/s?__biz=MzUyMzUyNzM4Ng==&mid=100001858&idx=1&sn=bd7345366a61a46d30d1aa85d63e2ab0&chksm=7a3a7df74d4df4e12a162f7a04ee5182154d009ff3fa4bb0e81155e1b3d1720851f8d07635e6&scene=18&ascene=7&devicetype=android-33&version=28002151&nettype=WIFI&abtest_cookie=AAACAA%3D%3D&lang=zh_CN&session_us=gh_6c6111156d8c&countrycode=CN&exportkey=n_ChQIAhIQrmC0P%2BEVy4w8YfzsS4sN1hLrAQIE97dBBAEAAAAAAGptFb7Eku8AAAAOpnltbLcz9gKNyK89dVj079xPHweohHib6dXGmlSiZApT%2FlH3RQTlTXYma7hdzTsM6tL0UyFb%2Fe70%2BPn8QrSRgJCzNXvByvnXm7w6D8eeqbNXVX92VkEj4E39yOWnT9fpIxnuanV9feTtI07VqrDAlc3uIz9kMJj3FeIQUnNIFaDcx548oWPqvvAbrvJLV8JJdN%2Bytw6wx81yMSFdT8LW8BOEFJYQbcdAp27%2FtGeq9i2r4PsXxh1Sn609mIhnJmZYhrvoRMlI9oSEETLsKceNHJZm07g%3D&pass_ticket=%2BHAP3q4K%2F58MUV3LqRV4jatlxOfkeAhkfn5GeDeCFSLanu7kv%2FMsRzJlbfh1cTG2b7NlungmQSbfm3TBnX4e%2BA%3D%3D&wx_header=3"
headers = {
    "Connection": "keep-alive",
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Linux; Android 13; M2102K1AC Build/TKQ1.220829.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/107.0.5304.141 Mobile Safari/537.36 XWEB/5023 MMWEBSDK/20230202 MMWEBID/752 MicroMessenger/8.0.33.2320(0x28002151) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
}

cookies = {
    "wxuin": "1206466542",
    "devicetype": "android-33",
    "version": "28002151",
    "lang": "zh_CN",
    "appmsg_token": "appmsg_token=1211_0muI7WhWOY9rDz0Tpe2uUOYxNG4P2ShovnXCjTKsc8tScNak2rmhITpC8j4~",
    "rewardsn": "",
    "wxtokenkey": "777",
    "pass_ticket": "+HAP3q4K/58MUV3LqRV4jatlxOfkeAhkfn5GeDeCFSIcwMpl0ZYvQEW2wBekmq7dEjmWyXIc2wahtYjKgwq1fA==",
    "wap_sid2": "CO7vpL8EEooBeV9ISFJvX3dteTZIcWZZNk1iaFh1RVZTV1BTYllsSmtVYmhnZTdKa1hybUYyeU5sWmxPZ3lqd2wxN0tNZ3Q2cjhJOHhrZWJQODl2aDBRek1BZlBWdkxBRlN2Vk5lRXNSbDl5LTdBVnlKVWlNVmltYWt1X2RGYm1GbDdHU3VYekxDRnFaa1NBQUF+MK2Wr6EGOA1AAQ=="
}


def get_params(mid, chksm, exportkey, sn, pass_ticket, idx=1):
    params = {
        "__biz": "MzUyMzUyNzM4Ng==",
        "mid": "{}".format(mid),
        "idx": "{}".format(idx),
        "chksm": "{}".format(chksm),
        "version": "28002151",
        "abtest_cookie": "AAACAA ==",
        "exportkey": "{}".format(exportkey),
        "sn": "{}".format(sn),
        "scene": "18",
        "devicetype": "android-33",
        "version": "28002151",
        "lang": "zh_CN",
        "nettype": "WIFI",
        "ascene": "7",
        "session_us": "gh_6c6111156d8c",
        "pass_ticket": "{}".format(pass_ticket),
        "wx_header": "3",
    }
    return params


def get_list_data(mid, chksm, exportkey, sn, pass_ticket,idx=1):
    res_html = requests.get(base_url, headers=headers, params=get_params(mid, chksm, exportkey, sn, pass_ticket,idx),
                            cookies=cookies)
    # print(res_html.text)
    soup = BeautifulSoup(res_html.text, "lxml")
    list = soup.find(id='js_content').find_all('a')
    for a in list:
        url = a.get('href')
        title = a.string
        if title is None:
            temp = a.find('span')
            if temp is not None:
                title = temp.string
        if title is None:
            title = "您还是自己看题目吧，爬取不到了！！！"+url
        insertDbItems(title, "没有图片", url)
        # print(title)
        # print(url)


if __name__ == '__main__':
    # 五个系列依次递增
    mids = [[100001858, "7a3a7df74d4df4e12a162f7a04ee5182154d009ff3fa4bb0e81155e1b3d1720851f8d07635e6",
             "n_ChQIAhIQme0s58UChzNbNhpdMdeeVhLrAQIE97dBBAEAAAAAAOoLC1Je0B0AAAAOpnltbLcz9gKNyK89dVj03voskk2H+FZ+2NAs+kahXrCWot9OOuAMc8hsVB6jApRwPZzjNhlE50h7zNreweNGbT4vx+3XVrL9xxPh2upzy+g+ftLD2fpP+tFYxkz2f8NkKewjqAn4AnAYx2r+NAW6WuaYoVvOFbsaeDsfUBgWMtf+0cUBS4oQugxK89q0Add4Dpf4idhleE9XOBZdh4G0NUBuKpJIYtsxvav9QDQ8QI+r3wouZWTYeiDVCm18L9CsAF4YtVJucOZWZ6pLPhuz1mdpvLA=",
             "bd7345366a61a46d30d1aa85d63e2ab0",
             "+HAP3q4K/58MUV3LqRV4jatlxOfkeAhkfn5GeDeCFSIqKF7aHTQcYcZjmtYUYcebgsHwj0VDscnMO2Q01Sqepg=="],
            [100003410, "7a3a7be74d4df2f1a0fb343acc563db2d55950581edaf8153a422d7c21f41ca5b79758a96e10",
             "n_ChQIAhIQ56Cv8teohCfpJ+0vFDanNxLrAQIE97dBBAEAAAAAAHQHIwqBdxUAAAAOpnltbLcz9gKNyK89dVj0SakmMCq2ytE9Pais1IfX7juvjHL5XGIvhwQWmi0IK+12xjpx8XRer1/8/cQJfyMSzuOqsIuX63EWOFsx73eg67ep4ouHnxHwEpMGg5fyJ2+FY90Q6Qmbp5yaA4Q3TlRq1JGKo7ByK8bHyMwC8vmyupaImIIFogCzjycO0qEkDVJDtIhaF0FU5/MgraF7J/rUgo/sV7/cmn0ALM1Mby/C2a1DHpkpwxa+y4uB4PwYhbpReVjXISVyYjLkCp+1MZpwYFHYBbY=",
             "4d72ae590a2c73c86c9ba35147e83432",
             "+HAP3q4K/58MUV3LqRV4jatlxOfkeAhkfn5GeDeCFSJug+AsyDoDOwAlEISZMM6XS431ZSMCe21VjwvIwwfKeg=="],
            [100005118, "7a3a614b4d4de85d3cab46324383c6d8500f920533c774c536ec74bfcc43844c95d05979c0c5",
             "n_ChQIAhIQgnLqQRrT9OdSHil0hG44BRLrAQIE97dBBAEAAAAAAIpdOdkwBywAAAAOpnltbLcz9gKNyK89dVj0OvY0yMRQgIZXF/hKfS16fCfitZw8wdj5i0NCTfuQacNGJd5CyfzWWgZZBP/RzPK9XEsOXfSpHDXoYjQogP0GrAz2JrEocG4LH5p08NsTlndi8YuFntMaEv+WEWzhxC5HOoW6WDF2jri/81CTqG7dXdx6SN+sAQTfZIULuQ3Gkp5g/BSy8oT3czNfyeJEXC+ck4cJfzXvqEB4H3XKmMNsmA9bwpAUCgUKjNWba6AE7Gex2Qm3HrZDdQEAj27bJi8OZVNU3Rc=",
             "1b3b3de88744b6504a20f1e35e5d6b55",
             "+HAP3q4K/58MUV3LqRV4jatlxOfkeAhkfn5GeDeCFSJP8Wo6wismdkwyGdRP+kxkJizMtaReVAOZmWOZiTiSZg=="],
            [100012844, "7a3986994d4e0f8f0f6fab78d5697c21a4fc10026a14bfcf08534039827139a3dfe04c04afbc",
             "n_ChQIAhIQNUBkm9C/osSfDfBMqxYMXBLrAQIE97dBBAEAAAAAAJRAKMflVuQAAAAOpnltbLcz9gKNyK89dVj0M5sGoyXjcnKK2AoGopRIPuT3e5nO2dxFcNA+yvFirHbHOZbX6JzQigfw6X3D8d0jpPMohS9kD7dQEPFOF2m6XEC4ByfqgmlxXqDbnN+GdIN20KgHtvI7myXvDSpGexlqODiZTEgqcaziCqlXWQThuDd41FKXZBN7H9vyiem2mdQah182TotKDFxcEfnX42zsmeh5Tee/XMGghQ/IYrDAPloSZvf50eKWEtkrcS0lsgH6RzxidpFOZeA3nukWaJu+8/TtDOs=",
             "209bb13d6f9a8c545bcee61ec392f431",
             "+HAP3q4K/58MUV3LqRV4jatlxOfkeAhkfn5GeDeCFSKWKoPY3zL6GAwSjht3Qgss0epLGzRSrZoc4ZfhckB+Ng=="],
            [2247512913, "fa39c6e4cd4e4ff2b2a69823fff5b5683f16d7edd1ddb03e1fd7be6c1e0c94b5cb1e5620af63",
             "n_ChQIAhIQNpil3j5YBLEFb5IBTZtqABLrAQIE97dBBAEAAAAAAJpVCFJOVXwAAAAOpnltbLcz9gKNyK89dVj08Q61DxLGbm/ACmlxeh+TmUDH9bKX+OhnDHO5DufSZUuzOXK35Jc3IYvHJ0bFRodgcvN5O2B3qYks+lG7dOuIl1ZB5/NqSICay2Li3VKuy+cvk9P3qLidmtsNMWQcDhgnC2kDXZ2NfPHguwibUj1+fTotzPIc5sSLSxJpG2go+swwmsaBW8+aIshRi0b0xE/XniDmX8B935rvdCKUHGlaOYHcWmK1XOXpmY7AVeduZyLAQI9BCBDaxpmOpTfOchliTZjTVqo=",
             "5b9f706abdaa97c117d818d8549ff006",
             "+HAP3q4K/58MUV3LqRV4jatlxOfkeAhkfn5GeDeCFSLas/jnEC4+UVSDqyh2/oUA7fTNP+mlcSjgPK8lpq+zNQ==",
             3]]
    for mid in mids:
        # print(mid[3])
        if len(mid)>5:
            get_list_data(mid[0], mid[1], mid[2], mid[3], mid[4], mid[5])
        else:
            get_list_data(mid[0], mid[1], mid[2], mid[3], mid[4])
        print(mid[0])
        print("=======================================================================")
    # get_list_data(mids[4][0], mids[4][1], mids[4][2], mids[4][3], mids[4][4], mids[4][5])
