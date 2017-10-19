# -*- coding: utf-8 -*-
"""
数据库管理类
"""
import ConfigParser
import traceback

import MySQLdb
from DBUtils.PooledDB import PooledDB
# 自定义的配置文件，主要包含DB的一些基本配置
import config


# 数据库实例化类
class DbManager:
    def __init__(self, config='../conf/spider163.conf'):
        cf = ConfigParser.ConfigParser()
        cf.read(config)
        host = cf.get("mysql", "host")
        username = cf.get("mysql", "username")
        password = cf.get("mysql", "password")
        database = cf.get("mysql", "database")

        connKwargs = {'host': host, 'user': username, 'passwd': password,
                      'db': database, 'charset': "utf8"}
        self._pool = PooledDB(MySQLdb, mincached=0, maxcached=10, maxshared=10, maxusage=10000, **connKwargs)

    def getConn(self):
        return self._pool.connection()

    # def getConn(self):
    #     _dbManager = DbManager()
    #
    #     """ 获取数据库连接 """
    #     return _dbManager.getConn()


    def executeAndGetId(self, sql, param=None):
        """ 执行插入语句并获取自增id """
        conn = self.getConn()
        cursor = conn.cursor()
        try:
            if param == None:
                cursor.execute(sql)
            else:
                cursor.execute(sql, param)
            conn.commit()
            id = cursor.lastrowid
        except Exception as err:
            conn.rollback()
            # 打印异常堆栈
            exstr = traceback.format_exc()
            print exstr
        finally:
            cursor.close()
            conn.close()

        return id

    def execute(self, sql, param=None):
        """ 执行sql语句 """
        conn = self.getConn()
        cursor = conn.cursor()
        try:
            if param == None:
                rowcount = cursor.execute(sql)
            else:
                rowcount = cursor.execute(sql, param)
            conn.commit()
        except Exception as err:
            conn.rollback()
            # 打印异常堆栈
            exstr = traceback.format_exc()
            print exstr
        finally:
            cursor.close()
            conn.close()

        return rowcount

    def batchInsertSQL(self, sql, values):
        conn = self.getConn()
        cursor = conn.cursor()
        cursor.execute("SET NAMES utf8mb4")

        try:
            cursor.executemany(sql, values)
            conn.commit()
        except Exception as err:
            print values
            conn.rollback()
            # 打印异常堆栈
            exstr = traceback.format_exc()
            print exstr
        finally:
            cursor.close()
            conn.close()

    def queryOne(self, sql):
        """ 获取一条信息 """
        conn = self.getConn()
        cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        rowcount = cursor.execute(sql)
        if rowcount > 0:
            res = cursor.fetchone()
        else:
            res = None
        cursor.close()
        conn.close()

        return res

    def queryAll(self, sql):
        """ 获取所有信息 """
        conn = self.getConn()
        cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        rowcount = cursor.execute(sql)
        if rowcount > 0:
            res = cursor.fetchall()
        else:
            res = None
        cursor.close()
        conn.close()

        return res


if __name__ == "__main__":
    dbManager = DbManager()

    # res = dbManager.execute('select id from rap_playlist163')
    # print str(res)
    #
    # res = dbManager.queryOne('select id from rap_playlist163')
    # print str(res)

    res = dbManager.queryAll('select id from rap_playlist163')
    print str(res)
