# -*- coding:utf-8 -*-
'''
用来爬取网易云音乐的所有top榜单
因为榜单名为中文，若将其作为表名会出很多问题，就将其转化为拼音+
'''
import lovesonglist
import requests
from bs4 import BeautifulSoup
from pypinyin import lazy_pinyin
headers = {
    'Referer': 'http://music.163.com/',
    'Host': 'music.163.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
}

def toplist():
    baseurl = 'http://music.163.com'
    URL = 'http://music.163.com/discover/toplist'
    topurllist = []
    topnamelist = []
    response = requests.get(URL,headers=headers).content
    soup =  BeautifulSoup(response,'html.parser')
    Toplist = soup.find_all(class_="s-fc0")
    for top in Toplist:
        topURL = baseurl + top.get('href')
        topnameEN = top.string
        #将榜单的中文名转化为拼音，用来作为表名
        aa = lazy_pinyin(topnameEN)
        topname = ''
        for a in aa:
            topname = topname+a
        if 'toplist' in topURL:
            print topname,topURL
            topurllist.append(topURL)
            topnamelist.append(topname)
    for i in xrange(len(topurllist)):
        list = lovesonglist.songlist(topurllist[i],listname=topnamelist[i])
        list.get_lovasonglist()

if __name__ == '__main__':
    toplist()
