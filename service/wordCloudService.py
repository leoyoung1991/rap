# encoding=utf8
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import jieba
from dao import db

from dao.db_manager import DbManager
import sys

reload(sys)
sys.setdefaultencoding('utf8')


class WordCloudService:
    def __init__(self, config="spider163.conf"):
        self.__db = db.MySQLDB()
        if config != "spider163.conf":
            self.__db.setConfig()
        self.dbManager = DbManager()

    def getChineseWords(self):
        sql = "select word from rap_word163 where rhyme like '%-%'"
        # words = self.__db.querySQL(sql)
        words = self.dbManager.queryAll(sql)
        wordList = []
        for word in words:
            # wordList.append(str(word))
            wordList.append(word.get('word'))
        return wordList

    def getWordCloud(self, results):
        print results
        wl_space_split = " ".join(results)

        # 修改WordCloud默认字体
        font = '/Users/luyang/code/workspace_py/rap/conf/simfang.ttf'
        my_wordcloud = WordCloud(font_path=font).generate(wl_space_split)
        # my_wordcloud = WordCloud().generate(wl_space_split)

        plt.imshow(my_wordcloud)
        plt.axis("off")
        plt.show()


if __name__ == "__main__":
    tmp = WordCloudService()
    results = tmp.getChineseWords()
    tmp.getWordCloud(results)
