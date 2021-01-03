# -*-coding:utf-8-*-
import  urllib2
from lxml import etree
class Record:
    def __init__(self):
        self.title=None
        self.type=None
        self.add = None
        self.money=None
        self.linkman=None
        self.detal=None

def download(url, user_agent='Mozilla/5.0' ,num_retries=2 ):
    print("Downloading!",url)
    headers = {"User-agent":user_agent}
    request = urllib2.Request(url,headers=headers)

    try:
        html=urllib2.urlopen(request).read()
        # print(html)
        title = etree.HTML(html).xpath('//h2/a[@target="_blank"]/text()')
        type = etree.HTML(html).xpath('//p[@class="room"]/text()')
        add = etree.HTML(html).xpath('//p[@class="add"]/a/text()')
        money = etree.HTML(html).xpath('//div[@class="money"]/b/text()')
        linkman = etree.HTML(html).xpath('//span[@class="listjjr"]/a[@href="javascript:;"]/text()')

        #     # linkman = etree.HTML(html).xpath('//div[@class="des"]//span/text()')
        detal = etree.HTML(html).xpath('//div[@class="des"]/h2/a/@href')
        # # print title[0], "!!", type[0], "!!", add[0], "!!", money[0], "!!", linkman[0], "!!", detal[0]
        print(title, "!!", type, "!!", add, "!!", money, "!!", linkman, "!!", detal)
        #
        # # 插入数据库

        # results = {'title':title,'type':type,'add':add,'money':money,'linkman':linkman,'detal':detal}
        print(title)
        print(len(title))
        i = 0
        records = []
        while i < len(title):
            record = Record()
            try:
                record.title = title[i]
            except:
                record.title='null'
            try:
                record.type = type[i]
            except:
                record.type = 'null'
            try:
                record.add = add[i]
            except:
                record.add ='null'
            try:
                record.money=money[i]
            except:
                record.money ='null'
            try:
                record.linkman=linkman[i]
            except:
                record.linkman ='null'
            try:
                record.detal=detal[i]
            except:
                record.detal ='null'
            i = i + 1
            records.append(record)

        # for info in records:
        #     print info.href, info.item, info.time
        from pymongo import MongoClient
        client = MongoClient('localhost', 27017)
        mydb = client.program
        record_collection = mydb.record
        for info in records:
            record = {'title': info.title,'type':info.type,'add':info.add,'money':info.money,'linkman':info.linkman,'detal':info.detal}
            record_collection.insert_one(record)


    except urllib2.URLError as e:
        print("url error:",e.reason)
        html=None
        if num_retries > 0:
            if hasattr(e,'code') and 500 <= e.code < 600:
                return download(url,user_agent,num_retries-1)
    return html



import re

def get_links(html):
    # 匹配所有<a>标签里面的href属性，暂时还没有匹配到的东西
    webpage_regex = re.compile('<a[^>]+class="next" href=["\'](.*?)["\']',re.IGNORECASE)

    return webpage_regex.findall(html)

def link_crawler(seed_url,link_regex):
    '''


    :param seed_url: 爬虫的起始URL
    :param link_regex: 爬取哪些链接的内容
    :return:
    '''
    # 爬取队列
    crawl_queue=[seed_url]
    seen = set(crawl_queue)

    # while len(crawl_queue)!=0:
    while crawl_queue:
        # 取出爬取队列里面的URL
        url = crawl_queue.pop()
        # 将取出的地址对应的页面下载下来
        html = download(url)

        for link in get_links(html):
            if re.match(link_regex,link):


                if not link in seen:
                    seen.add(link)
                    crawl_queue.append(link)


link_crawler("http://dl.58.com/chuzu/pn1/","/chuzu/pn|")

