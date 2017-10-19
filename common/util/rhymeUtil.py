# -*- coding: utf-8 -*-

class RhymeUtil:
    def __init__(self):
       pass

    @staticmethod
    def getWordRhyme(pinyin):

        separator = '-'
        vowelList = ['a', 'e', 'i', 'o', 'u']

        # aeiou 作为字的分界， 包含及后面的为韵脚    default splitter is `-`

        strlist = pinyin.split(separator)
        defaultPos = -1
        rhymeList = []
        for value in strlist:
            print value
            pos = defaultPos
            for c in vowelList:

                temp = value.find(c)

                if temp == defaultPos:
                    continue
                else:
                    if pos == defaultPos:
                        pos = temp
                    else:
                        if pos > temp:
                            pos = temp

            rhyme = value[pos:]
            rhymeList.append(rhyme)

        rhyme = separator.join(rhymeList)
        print rhyme
        return rhyme
