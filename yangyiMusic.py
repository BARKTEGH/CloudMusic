#-*- coding:utf-8 -*-
'''
class musicdetail 为一首歌的信息和评论
'''
import requests
from bs4 import BeautifulSoup
import json
import Mysql
import music_comment
import time
headers = {
    'Referer': 'http://music.163.com/',
    'Host': 'music.163.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
}
proxies = {
    "https": 'http://27.18.110.254:808',
    "https": 'http://122.237.28.118:808',
    "https": 'http://180.124.2.224:808',
    "https": 'http://60.168.35.11:808',
    "https": 'http://223.244.155.188:808',
    "https": 'https://115.220.5.18:808'
}
mysql = Mysql.Mysql()
class musicdetail(object):
    '''
    <em class="f-ff2">Shape of You</em>
    <a title="播放mv" href="/mv?id=5439044"><i class="icn u-icn u-icn-2"></i></a>
    </div>
    </div>
    <p class="des s-fc4">歌手：<span title="Ed Sheeran"><a class="s-fc7" href="/artist?id=33184">Ed Sheeran</a></span></p>
    <p class="des s-fc4">所属专辑：<a href="/album?id=35114127" class="s-fc7">Shape Of You</a></p>
    '''
    def __init__(self,id):
        self.url = 'http://music.163.com/song?id=' + str(id)  #注意去掉 #/
        self.baseurl = 'http://music.163.com'
        self.songID = id
        self.music_name = ''
        self.music_artist = ''
        self.music_MV = ''
        self.music_album= ''
        self.music_lyric = ''
        self.music_comment = {}
        self.head = headers

    def get_page(self):
        response = requests.get(self.url,headers=self.head,proxies=proxies).content.decode('utf8')
        return response

    def music_item(self,response):
        soup = BeautifulSoup(response,'html.parser')
        #get music name
        self.music_name =soup.find(class_="f-ff2").string
        #get mv URL
        MVurl = soup.find(title="播放mv").get('href')
        if MVurl == None:
            self.music_MV = 'no MV'
        else:
            self.music_MV = self.baseurl + MVurl

        musicitems = soup.find_all(class_="s-fc7")
        try:
            self.music_artist = musicitems[1].string
            self.music_album = musicitems[2].string
        except:
            self.music_artist = ' no artist'
            self.music_album = 'no album'

        return self.music_name,self.music_MV,self.music_artist,self.music_album

    def music_lyric(self):
        csrf_token='1434df05efaa64153c6ade083e403fe2'
        lyric_url = 'http://music.163.com/weapi/song/lyric?csrf_token='+csrf_token
        response = requests.post(lyric_url,headers=self.head)
        lyric_json = json.loads(response)
        if lyric_json == None:
            self.music_lyric = 'no lyric'
        else:
            self.music_lyric = lyric_json['lrc']['lyric']

    def music_Comment(self):
        id = self.songID
        self.music_comment = music_comment.get_comment(id)
        return self.music_comment

    def save_music_items(self):
        table = 'music_items'
        dict = {
            'musicID':self.songID,
            'musicURL':self.url,
            'musicName':self.music_name,
            'musicArtist':self.music_artist,
            'musicAlbum':self.music_album,
            'musicMV':self.music_MV
        }
        mysql.insertData(table,dict)
        print time.ctime(),'歌曲ID:',self.songID,'信息保存完毕'

    def save_comment(self):
        table = 'musiccomment'
        for i in self.music_comment:
            dict = {
                    'music_user_id':self.songID+'+'+i,
                    'hostcomment':self.music_comment[i]}
            mysql.insertData(table,dict)
        print time.ctime(),'歌曲ID:',self.songID,'热门评论保存完毕'

    def run(self):
        response = self.get_page()
        self.music_item(response)
        #得到热门评论
        self.music_Comment()
        #将歌曲信息存入数据库中
        self.save_music_items()
        #将热门评论存入数据库中
        self.save_comment()
        #print self.music_name,self.music_MV,self.music_artist,self.music_album
        return self.music_name,self.music_MV,self.music_artist,self.music_album,self.music_comment

def main():
    music= musicdetail('460043746')
    music.run()

if __name__=='__main__':
    main()










