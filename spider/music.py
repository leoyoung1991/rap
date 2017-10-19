#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import re
import threading
import traceback
import urllib2

import requests
import time
from bs4 import BeautifulSoup
import MySQLdb
import json
import common.common as c
from dao import db
from dao.db_manager import DbManager


class Music:
    def __init__(self, config="spider163.conf"):
        self.__headers = {
            'Referer': 'http://music.163.com/',
            'Host': 'music.163.com',
            # 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) '
            #               'Chrome/55.0.2883.95 Safari/537.36',

            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        }
        self.__db = db.MySQLDB()
        if config != "spider163.conf":
            self.__db.setConfig()
        self.__url = "http://music.163.com"

        self.lyricAPI = 'http://music.163.com/api/song/lyric?os=pc&lv=-1&kv=-1&tv=-1&id='
        self.multyNum = 2
        self.sleepTime = 10

        self.dbManager = DbManager()

        self.allValidIp = self.getAllValidIp()

    def getAllSongList(self):
        sql = "select link from rap_playlist163 where status in (0,1,9)"
        return self.__db.querySQL(sql)

    def geneAllSongs(self, results):
        lens = len(results)
        threads = []

        for link in results:
            t = threading.Thread(target=self.getOneSongList, args=link)
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
        print '获取歌曲线程全部启动成功。。。'
        # t.join()
        # 等待子线程结束

        for t in threads:
            t.join()

    def getOneSongList(self, songListlink):
        global content, lyric
        s = requests.session()
        url = self.__url + str(songListlink)

        # request = urllib2.Request(url=url, headers=self.__headers)
        # response = urllib2.urlopen(request)
        # page = response.read().decode('utf-8')
        b = random.sample(self.allValidIp, 1)
        proxy = b[0]

        try:

            try:
                content = s.get(url, headers=self.__headers, proxies=proxy).content
            except:
                # 将这个代理去掉
                # self.allValidIp.remove(proxy)
                # 改变状态到歌曲获取失败
                self.dbManager.execute(
                    "update rap_playlist163 set status = 9 where link = '" + str(songListlink) + "'")

                return

                # content = s.get(url).content
            # s = BeautifulSoup(page, "lxml")

            page = BeautifulSoup(content, "lxml")
            musics = page.find('ul', {'class': 'f-hide'})

            if musics is None:
                # 将这个代理去掉
                # self.allValidIp.remove(proxy)
                # 改变状态到歌曲获取失败
                self.dbManager.execute(
                    "update rap_playlist163 set status = 9 where link = '" + str(songListlink) + "'")
                print '%s return 503' % songListlink

                return

            # 先改变状态到生成歌曲中， 锁住
            self.dbManager.execute(
                "update rap_playlist163 set status = 1 where status = 0 and link = '" + str(songListlink) + "'")

            # 一次插入多条记录
            sql = "insert into rap_music163 (`song_id`, `name`, `link`, `lyric`, `status`)" \
                  "values(%s,%s,%s,%s,%s)"
            status = 1
            values = []
            for music in musics:
                songLink = MySQLdb.escape_string(music.find('a')['href'].encode('utf-8'))
                name = MySQLdb.escape_string(music.text.encode('utf-8'))
                o = re.match(r'.*id=(.*)', songLink, re.M | re.I)
                id = int(o.group(1))

                # 根据songLink获取歌词
                lrc_url = self.lyricAPI + str(id)


                try:
                    lyric = s.get(lrc_url, headers=self.__headers, proxies=proxy)
                except:
                    # 将这个代理去掉
                    # self.allValidIp.remove(proxy)
                    # 改变状态到歌曲获取失败
                    # self.dbManager.execute(
                    #     "update rap_playlist163 set status = 9 where link = '" + str(songListlink) + "'")

                    return

                time.sleep(0.5)  # 休眠0.1秒

                json_obj = lyric.text
                j = json.loads(json_obj)
                code = j['code']
                if code == 200 and j.has_key('lrc') and j['lrc'].has_key('lyric'):
                    lrc = j['lrc']['lyric']
                    pat = re.compile(r'\[.*\]')
                    lrc = re.sub(pat, "", lrc)
                    lrc = lrc.strip()
                    # print(lrc)

                    if not self.isDuplicate(songLink):
                        values.append((id, name, songLink, lrc, status))
                        print name

            # 由于有歌词 所以存在sql过长问题
            self.dbManager.batchInsertSQL(sql, values)
            print values

            # 再改变状态到生成歌曲完成
            self.dbManager.execute(
                "update rap_playlist163 set status = 2 where status =1 and link = '" + str(songListlink) + "'")


        except Exception as err:
            # 打印异常堆栈
            exstr = traceback.format_exc()
            print exstr
            c.Log('{} : {}'.format("Error 901", err))

    def isDuplicate(self, songLink):
        sql = "select * from rap_music163 where link = '" + str(songLink) + "'"
        # result = self.__db.querySQL(sql)

        result = self.dbManager.queryOne(sql)
        if result is None:
            return False
        return True

    def getAllValidIp(self):
        f = open("../common/antiSpider/ipProxy/valid_proxy")
        lines = f.readlines()
        proxys = []
        for i in range(0, len(lines)):
            ip = lines[i].strip("\n").split(":")
            proxy_host = "http://" + ip[0] + ":" + ip[1]
            proxy_temp = {"http": proxy_host}
            proxys.append(proxy_temp)
        return proxys


if __name__ == "__main__":
    tmp = Music()

    results = tmp.getAllSongList()
    tmp.geneAllSongs(results)

    # tmp.viewCapture("/playlist?id=739396417")
