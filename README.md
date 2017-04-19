# CloudMusic
爬取网易云音乐歌曲

<br>music_comment 为通过传入歌曲ID，爬取每一首歌的热评，返回热评
     可以在里面稍作修改,获得所有评论</br>
 <br>yangyiMusic 为获取一首歌的详细信息，比如歌名，ID，歌手，专辑等等，并将其存入数据库中</br>
 <br>lovesonglist  用来获取歌单中每首歌的ID等等信息,并将每个歌单以表的形式存储下来.</br>
 
database：
 cloudmusic：
   table： music_items 存储每首歌的信息
          musiccomment  存储每首歌的热评
          
          lovesonglist  存储 最喜爱的歌曲歌单 歌单模板都相同
          billboard    billboard周榜
          uk              uk周榜
