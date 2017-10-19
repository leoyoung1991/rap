# -*- coding: utf-8 -*-

import time
from pyExcelerator import *
# excel 第一行数据
excel_headDatas = [u'发布时间', u'文章标题', u'文章链接', u'文章简介']
articles =[
    {u'发布时间':u'2017年5月9日',
     u'文章标题':u'Python项目实战教程：国内就能访问的google搜索引擎',
     u'文章链接':'http://mp.weixin.qq.com/s?timestamp=1494557315',
     u'文章简介':u'大家可以留言、想了解python那个方向的知识、不然我也不知道'},

    {u'发布时间':u'2017年5月4日',
     u'文章标题':u'对于学习Django的建议、你知道的有那些',
     u'文章链接':'http://mp.weixin.qq.com/s?timestamp=1494557323',
     u'文章简介':u'随着Django1.4第二个候选版的发布，虽然还不支持Python3，但Django团队已经在着手计划中，据官方博客所说，Django1.5将会试验性的支持python3'}
]
# 定义excel操作句柄
excle_Workbook = Workbook()
excel_sheet_name = time.strftime('%Y-%m-%d')
excel_sheet = excle_Workbook.add_sheet(excel_sheet_name)
index = 0
#标题
for data in excel_headDatas:
    excel_sheet.write(0, index, data)
    index += 1

index = 1

#内容
for article in articles:
    colIndex = 0
    for item in excel_headDatas:
        excel_sheet.write(index, colIndex, article[item])
        colIndex += 1
    index += 1
#保存test.xlsx到当前程序目录
excle_Workbook.save('test.xls')

# db = mongoDB.mongoDbBase()
# db.Get_information_stat()