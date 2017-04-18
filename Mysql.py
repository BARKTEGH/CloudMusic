# -*- coding:utf-8 -*-
import MySQLdb
import time

class Mysql(object):

    def __init__(self):
        try:
            self.db = MySQLdb.connect('127.0.0.1','root','*******','cloudmusic')
            print '链接数据库test成功'
            self.cur = self.db.cursor()
        except MySQLdb.Error, e:
            print time.ctime(),'链接数据库错误，原因%d: %s ' % (e.args[0], e.args[1])

    def insertData(self,table, my_dict):
        try:
            self.db.set_character_set('utf8')
            cols = ','.join(my_dict.keys())
            values = '","'.join(my_dict.values())
            sql = "INSERT INTO %s (%s) VALUES (%s)"  % (table, cols, '"'+values+'"')
            try:
                result = self.cur.execute(sql)
                insert_id = self.db.insert_id()
                self.db.commit()
                if result:
                    return insert_id
                else:
                    return 0
            except MySQLdb.Error, e:
                self.db.rollback()
                if "key 'PRIMARY' " in e.args[1]:
                    print time.ctime(), '数据已存在'
                else:
                    print time.ctime(),'插入数据失败，原因 %d: %s' % (e.args[0], e.args[1])
        except MySQLdb.Error, e:
            print time.ctime(), "数据库错误，原因%d: %s" % (e.args[0], e.args[1])

