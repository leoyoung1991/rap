#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String, DateTime, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.sql import func
from sqlalchemy.dialects.mysql import MEDIUMTEXT
import config

Base = declarative_base()


class Playlist163(Base):
    __tablename__ = "rap_playlist163"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    title = Column(String(150), server_default="")
    link = Column(String(120), server_default="")
    play_num = Column(String(20), server_default="")
    create_time = Column(DateTime, server_default=func.now())
    status = Column(Integer(), server_default="0")


class Music163(Base):
    __tablename__ = "rap_music163"
    id = Column(Integer(), primary_key=True, autoincrement=True)
    song_id = Column(Integer())
    name = Column(String(200), server_default="")
    link = Column(String(120), server_default="")
    lyric = Column(MEDIUMTEXT)
    create_time = Column(DateTime, server_default=func.now())
    status = Column(Integer(), server_default="0")
    key_author = Index("link", link)
    key_author = Index("status", status)


class Word163(Base):
    __tablename__ = "rap_word163"
    id = Column(Integer(), primary_key=True, autoincrement=True)
    word = Column(String(20), server_default="")
    count = Column(Integer())
    pinyin = Column(String(30), server_default="")
    rhyme = Column(String(30), server_default="")
    create_time = Column(DateTime, server_default=func.now())
    status = Column(Integer(), server_default="0")


engine = create_engine(config.get_db(), convert_unicode=True, echo=True)


def single(table, k, v):
    cnt = engine.execute('select count(*) from ' + table + ' where ' + k + '="' + v + '"').fetchone()
    if cnt[0] == 0:
        return True
    else:
        return False


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    print(single("playlist163", "link", "sd"))
