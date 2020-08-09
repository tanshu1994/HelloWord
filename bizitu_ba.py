# !/bin/bash
# author: Ts

from bs4 import BeautifulSoup
import requests
import io
import os
import time
'''
    彼岸桌面壁纸图.你值得拥有.
'''

# 伪装浏览器标识
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36"
}
mainUrl = "http://www.netbian.com" #彼岸桌面壁纸主页.

#文件保存路径(这里要改成你要下载的目录路径.)
savePath = "C:\\Users\\Administrator\\Desktop\\zgsjz\\background\\"

hrefs = []
texts = []
session = requests.session()  # 实例化session

def main(url):
    session.headers.update(headers)
    r = session.get(url)
    soup = BeautifulSoup(r.content, 'lxml')
    alist = soup.find(attrs={"class": "nav cate"}).find_all("a")  # 获取所有子a标签.
    i = 0;
    for item in alist:
        if item.get("href") == 'http://pic.netbian.com/': continue  # 如果是4K壁纸
        hrefs.append(item.get("href"))
        texts.append(item.get_text() + ":" + str(i))
        i += 1
    print(texts)
    # 请输入类型.开始下载.
    index = input("请输入下载的壁纸类型编号:")
    st = input("请您输入开始下载的页码(整数):")
    ed = input("请您输入结束下载的页码(整数):")
    # index = 3  # 下标.(默认美女)
    url = mainUrl + hrefs[int(index)]
    start(url, int(st), int(ed))

def start(url, st, ed):
    if st < 1:
        print("开始页码不能小于1")
        return
    queue = [i for i in range(st, ed)]  # 构造url链接页码
    pageUrl = url + "/index_{}.htm"
    while len(queue) > 0:
        print("开始下载:")
        num = queue.pop(0)
        if num == 1:
            download(url)
        else:
            url = pageUrl.format(num)
            print(url)
            download(url)

#下载一个页面的壁纸.
def download(url):
    r = session.get(url)
    soup = BeautifulSoup(r.content, 'lxml')

    #拿到每一个ul
    ul = soup.find(attrs={"class": "list"}).find('ul')
    print("下载开始ul-->>")

    href0s = []
    for li in ul:
        # print(li)
        href0 = li.find("a").get("href")
        # print(href0)
        if href0 != "http://pic.netbian.com/":
            href0s.append(mainUrl + href0)
    # 定义新的进入路径
    print(href0s)

    for url in href0s:
        r = session.get(url)
        try:
            if r.status_code == 200:
                soup = BeautifulSoup(r.content, 'lxml')
                a = soup.find("p").find("a")  # 获取二级a标签
                name = a.find('img').get("alt")
                href = a.get("href")
                url = mainUrl + href
                time.sleep(1)
                if os.path.exists(savePath + name + '.jpg'):
                    print(name+",文件已经存在,跳过本次下载呢.")
                    continue
                r = session.get(url)
                if r.status_code == 200:
                    soup = BeautifulSoup(r.content, 'lxml')
                    src = soup.find("table").find("tr").find("td").find("a").get("href")
                    time.sleep(1)
                    r = session.get(src)
                    if r.status_code == 200:
                        print("download:" + name)
                        open(savePath + name + '.jpg', 'wb').write(r.content)  # 将内容写入图片
                        print("success"+ name)
        except:
            print("发生了异常")

if __name__ == '__main__':
    main(mainUrl)