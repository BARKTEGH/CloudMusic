# -*- coding:utf-8 -*-
import yangyiMusic
import requests
from bs4 import BeautifulSoup
import json
import Mysql
import time

headers = {
    'Referer': 'http://music.163.com/',
    'Host': 'music.163.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
}
#url = 'http://music.163.com/#/playlist?id=30492073'
class songlist(object):
    def __init__(self,listurl,listname='Billboard'):
        self.URL = listurl
        self.listname = listname
        self.mysql = Mysql.Mysql()

    def get_lovasonglist(self):
        print time.ctime(),'开始爬取歌单'
        self.creat_table()
        response = requests.get(self.URL,headers=headers).content
        soup= BeautifulSoup(response,'html.parser')
        textarea = soup.find('textarea').text
        musiclist = json.loads(textarea)
        for music in musiclist:
            songName = music["name"]
            print '歌曲为:',songName
            songid = str(music["privilege"]["id"])
            song = yangyiMusic.musicdetail(songid)
            song.run()
            songURL = 'http://music.163.com/song?id=' + songid
            albumName = music["album"]["name"]
            artistName = music["artists"][0]["name"]
            artistID = str(music["artists"][0]["id"])
            self.save_list_to_mysql(songid,songURL,songName,albumName,artistName,artistID)
        return 0

    def creat_table(self):
        sql = 'SELECT COUNT(*) FROM information_schema.TABLES WHERE TABLE_NAME="%s"' % self.listname.lower()
        self.mysql.cur.execute(sql)
        b = self.mysql.cur.fetchone()[0]
        if b == 0:
            print '创建表'
            sql2= 'CREATE TABLE' +self.listname.lower()+ 'LIKE billboard';
            self.mysql.cur.execute(sql2)
        else:
            print self.listname,'表已经存在'

    def save_list_to_mysql(self,songid,songURL,songName,albumName,artistName,artistID):
        table = self.listname
        dict ={
            'songid':songid,
            'songURL':songURL,
            'songName':songName,
            'albumName':albumName,
            'artistName':artistName,
            'artistID':artistID
        }
        self.mysql.insertData(table,dict)
        print time.ctime(),'歌曲:',songName,'存入歌单成功'
        print '--------'
        return 0


def main():
    list = songlist('http://music.163.com//discover/toplist?id=180106',listname='UK')
    list.get_lovasonglist()

if __name__ == '__main__':
    main()
