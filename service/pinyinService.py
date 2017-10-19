# -*- coding: utf-8 -*-
import threading

import time
import traceback
import common.common as c
import jieba

from common.util.rhymeUtil import RhymeUtil
from dao import db

import redis

from dao.db_manager import DbManager
from service.wordService import WordService
from xpinyin import Pinyin
import sys

reload(sys)
sys.setdefaultencoding('utf8')


class PinyinService:
    def __init__(self, config="spider163.conf"):
        self.__db = db.MySQLDB()
        if config != "spider163.conf":
            self.__db.setConfig()

        self.pool = redis.ConnectionPool(host='127.0.0.1', port='6379')
        self.r = redis.Redis(connection_pool=self.pool)
        self.step = 10

        self.dbManager = DbManager()


    def genePinyinAndSave(self):

        try:

            wordService = WordService()
            countWords = self.r.zcard(wordService.sortedSetKey)
            print countWords

            p = Pinyin()

            i = 0
            while i < countWords:
                wordCounts = self.r.zrange(wordService.sortedSetKey, i, i + self.step, desc=False, withscores=True,
                                           score_cast_func=int)
                # 入mysql

                # 一次插入多条记录
                sql = "insert into rap_word163 (`word`, `count`, `pinyin`, `rhyme`, `status`)" \
                      "values(%s,%s,%s,%s,%s)"
                status = 1
                values = []

                for wordCount in wordCounts:

                    word = wordCount[0]
                    count = wordCount[1]

                    if not self.isDuplicate(word):
                        pinyin = ''
                        try:
                            # 获取拼音
                            # default splitter is `-`
                            pinyin = p.get_pinyin(unicode(word, "utf-8"))
                        except Exception as err:
                            # 打印异常堆栈
                            exstr = traceback.format_exc()
                            print exstr
                            continue

                        # 获取韵脚
                        rhyme = RhymeUtil.getWordRhyme(pinyin)

                        values.append((word, count, pinyin, rhyme, 0))

                # 由于有歌词 所以存在sql过长问题
                self.dbManager.batchInsertSQL(sql, values)
                time.sleep(0.5)
                print 'save %s - %s words' % (i, i + self.step)
                i += self.step

        except Exception as err:
            # 打印异常堆栈
            exstr = traceback.format_exc()
            print exstr


    def isDuplicate(self, name):
        sql = "select * from rap_word163 where word = '" + str(name) + "'"
        # result = self.__db.querySQL(sql)

        result = self.dbManager.queryOne(sql)
        if result is None:
            return False
        return True

if __name__ == "__main__":
    tmp = PinyinService()
    tmp.genePinyinAndSave()
