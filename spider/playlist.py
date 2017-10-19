#!/usr/bin/env python
# -*- coding: utf-8 -*-
import traceback

import requests
from bs4 import BeautifulSoup
import MySQLdb
import common.common as c
from dao import db


class Playlist:
    __db = None
    __play_url = None
    __headers = None

    def __init__(self, config="../conf/spider163.conf"):
        self.__headers = {
            'Referer': 'http://music.163.com/',
            'Host': 'music.163.com',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        }
        self.__db = db.MySQLDB()
        if config != "../conf/spider163.conf":
            self.__db.setConfig()
        self.__play_url = "http://music.163.com/discover/playlist/?order=hot&cat=说唱&limit=35&offset="

        self.totalPage = 39

    def getOnePageSongList(self, page):
        s = requests.session()
        play_url = self.__play_url + str(page * 35)
        try:
            s = BeautifulSoup(s.get(play_url, headers=self.__headers).content, "lxml")
            lst = s.find('ul', {'class': 'm-cvrlst f-cb'})

            values = []
            # 一次插入多条记录
            sql = "insert into rap_playlist163 (`title`, `link`, `play_num`)" \
                  "values(%s,%s,%s)"

            for play in lst.find_all('div', {'class': 'u-cover u-cover-1'}):
                title = MySQLdb.escape_string(play.find('a', {'class': 'msk'})['title'].encode('utf-8'))
                link = MySQLdb.escape_string(play.find('a', {'class': 'msk'})['href'].encode('utf-8'))
                playNum = MySQLdb.escape_string(play.find('span', {'class': 'nb'}).text.encode('utf-8'))

                values.append((title, link, playNum))

            self.__db.batchInsertSQL(sql, values)
            print 'page:%s页 歌单入库' % page

        except Exception as err:
            # 打印异常堆栈
            exstr = traceback.format_exc()
            print exstr
            c.Log('{} : {} {}'.format("ERROR 104 ", "URL", play_url))

    def getAllSongList(self):

        for i in range(1, self.totalPage):
            self.getOnePageSongList(i)


if __name__ == "__main__":
    tmp = Playlist()
    tmp.getAllSongList()
