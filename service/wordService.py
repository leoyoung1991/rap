# -*- coding: utf-8 -*-
import threading

import time
import traceback
import common.common as c
import jieba
from dao import db

import redis

from dao.db_manager import DbManager


class WordService:
    def __init__(self, config="spider163.conf"):
        self.__db = db.MySQLDB()
        if config != "spider163.conf":
            self.__db.setConfig()
        self.multyNum = 2
        self.sleepTime = 0.5

        self.pool = redis.ConnectionPool(host='127.0.0.1', port='6379')
        self.r = redis.Redis(connection_pool=self.pool)
        self.sortedSetKey = 'word'

        self.dbManager = DbManager()


    def getAllSongs(self):
        sql = "select lyric, id from rap_music163 where status = 1 or status = 2"
        return self.__db.querySQL(sql)

    def geneAllWords(self, results):

        lens = len(results)
        threads = []

        for music in results:
            t = threading.Thread(target=self.getOneSong, args=(music[0], music[1]) )
            threads.append(t)

        i = 0
        for t in threads:
            t.setDaemon(True)
            t.start()
            # 多线程并发+休息
            i += 1
            if i >= self.multyNum:
                time.sleep(self.sleepTime)
                i = 0
        print '抓取所有地铁站附近房源线程全部启动成功。。。'

        for t in threads:
            t.join()

    def getOneSong(self, lyric, id):

        try:
            # 先改变状态到生成歌曲中， 锁住
            self.dbManager.execute("update rap_music163 set status = 2 where status = 1 and id = '" + str(id) + "'")

            # 结巴分词
            print len(lyric)

            # 打开并行
            # jieba.enable_parallel(4)
            # 关闭并行
            jieba.disable_parallel()

            words = [x for x in jieba.cut(lyric) if len(x) >= 2]
            jieba.disable_parallel()
            from collections import Counter
            count = Counter(words).most_common(20)
            print count

            for vo in count:
                word = vo[0]
                number = vo[1]
                # 自增有序集合内value对应的分数
                self.r.zincrby(self.sortedSetKey, word, number)  # 自增zset_name对应的有序集合里a1对应的分数

            print self.r.zcard(self.sortedSetKey)


            # # 获取关键词
            # tags = jieba.analyse.extract_tags(lyric, topK=3)
            # print u"关键词:"
            # print " ".join(tags)


            # 循环每个词，数据库里确认是插入还是更新   redis更好

            self.dbManager.execute("update rap_music163 set status = 3 where status = 2 and id = '" + str(id) + "'")



        except Exception as err:
            # 打印异常堆栈
            exstr = traceback.format_exc()
            print exstr
            c.Log('{} : {}'.format("Error 901", err))


if __name__ == "__main__":
    tmp = WordService()
    results = tmp.getAllSongs()
    tmp.geneAllWords(results)
