# -*- coding: utf-8 -*-
import json
import traceback
import urllib
import urllib2

import time
from pyExcelerator import *


class SlowSQL3:
    def __init__(self):
        self.slowSQLURL = 'https://clouddba.alibaba-inc.com/db/slowsql/modules/topSql.do?_input_charset=utf-8&_tb_token_=2cOxFuZB1lwcni8zHIoL&token=51fcbf68-abc5-4bcd-8cbe-d3649f5ce1c1&setDb=false&sort=&order=&'
        self.total = 473
        self.pageSize = 20
        self.startTime = '2017-10-10 15:00:00'
        self.endTime = '2017-10-17 15:59:59'
        self.rows = 20
        self.opener = urllib2.build_opener()
        self.opener.addheaders.append(('Cookie',
                                       'clouddba-web_USER_COOKIE=1B26963AA530BBB8BF1C472638445D86CD08EE20473BF9DD2B5E56F98B131CF82BCFEFDE1CF8140BCC152AFE609928109FE52F8AD954025B8B363479C43FBC022C5BD16AAF39B0C88BDA2A0D860F8F2FE69C794AAF3479AE3D94B42690F3D1BAF8ABE19D7216ACC85FCB9433166972C9B415CA99243D054D947F46B9003D994761093835D078E8728BBB81B636510A7595A7E07F65422BA2DE94BA3CF01F81B3401F8BAADBCABA3C9E46D82D154A3DFFD3AF1150A4EF9E5AD30FD43FCC9FD2CBF472E5078E5061E2CDFB6ADE68280D981BCFC57CE458FA813F2CB9AC4D5CD2AD927A39CD5E5E0C3D23BB4DF5F5E28CFBF760B271E71CDABFEA7FA34BB3853B6EB7C0AD821691D3C98ED4DF14280AE193AEFF255D5AE58A72B7C2392971B8090B749987AA651D1FEC006519496CED3E7CCE7C7BAFB53828E54DCF923003A444516132DA16AA21AFE27AEF7834D481F472C79E446C133F326AAB4C37F197D328D857AB33740114241B86DE74CD4F2F1919CF005D0D96532D8537CEEC6498EC197FD3FF352A40EEB38AD8CD982AC33570DA; clouddba-web_SSO_TOKEN=BB8DDB7131E7C59C7DF9AB1F35A801782BC2A74A011226D2BDE475958DA6F0842EE0C11C5218342CAC8AB471D04AFDCF; clouddba-web_LANG=zh-CN; clouddba-web_LAST_HEART_BEAT_TIME=76B71D3EAB8836708EA23BB3D397B8DC; __CloudDBA_USER_TOKEN_KEY_=ed20a4d4-6035-4a4e-adfe-9f596989ab52; UM_distinctid=15f2e01f769991-0802eddc727d94-31627c00-13c680-15f2e01f76ace4; cna=+ddtEvfySTECAYzNHAhqB9eb; isg=AnFxLJM5jOYS_SDyKslnalZpgPsVK_18VEvzgVOGoDhwepPMm62EoH7Y6jjn'))

        self.excel_headDatas = [u'格式化sql', u'实际执行sql', u'sqlTag', u'平均执行时间', u'平均排队时间', u'平均扫描行', u'平均返回行', u'平均变更行',
                                u'clouddba建议', u'周执行次数']

    @property
    def getLatestWeekSlowLog(self):

        values = []
        pageNum = self.total / self.pageSize + 1
        for i in range(pageNum):
            try:
                params = urllib.urlencode(
                    {'page': str(i), 'startTime': self.startTime, 'endTime': self.endTime, 'rows': self.rows})
                url = self.slowSQLURL + params
                f = self.opener.open(url)
                print 'url : %s' % url
                content = f.read()
                print 'content : %s' % content
                j = json.loads(content)
                success = j['success']

                if success == True and j.has_key('root') and j['root'].has_key('rows'):
                    rows = j['root']['rows']
                    print rows
                    for row in rows:
                        if row['avgQueryTime'] - row['avgQueueTime'] >= 1:
                            print (row['avgLockTime'], row['avgLrPagesRead'], row['avgQueryTime'], row['avgQueueTime'],
                                   row['avgRowsAffected'], row['avgRowsExamined'], row['avgRowsSent'], row['checksum'],
                                   row['dbName'], row['dbRole'], row['formatSql'], row['ip'], row['maxLockTime'],
                                   row['maxQueryTime'], row['maxRowsExamined'], row['maxRowsSent'], row['port'],
                                   row['sqlId'],
                                   row['sqlTag'], row['sqlText'], row['sqlType'], row['sumCount'], row['sumCountPct'],
                                   row['sumLockTime'], row['sumLrPagesRead'], row['sumQueryTime'], row['sumQueueTime'],
                                   row['sumRowsAffected'], row['sumRowsExamined'], row['sumRowsSent'])
                            values.append((row['formatSql'], row['sqlText'], row['sqlTag'], row['avgQueryTime'],
                                           row['avgQueueTime'],
                                           row['avgRowsExamined'], row['avgRowsSent'], row['avgRowsAffected'],
                                           self.transform(row['sqlTag']), row['sumCount']))
                time.sleep(3)
            except Exception as err:
                exstr = traceback.format_exc()
                print exstr

        return values

    def transform(self, sqlTag):
        # "FAST": "非慢查询",
        # "LOCKED": "锁阻塞",
        # "QUEUED": "系统忙",
        # "WAIT": "被影响",
        # "OPTIMAL_DML": "优化空间不大",
        # "SUSPICIOUS_DML": "可疑查询",
        # "NEGLIGIBLE_DML": "低频查询",
        # "DDL": "DDL",
        # "OTHER": "未识别语句"

        switcher = {
            "FAST": u"非慢查询",
            "LOCKED": u"锁阻塞",
            "QUEUED": u"系统忙",
            "WAIT": u"被影响",
            "OPTIMAL_DML": u"优化空间不大",
            "SUSPICIOUS_DML": u"可疑查询",
            "NEGLIGIBLE_DML": u"低频查询",
            "DDL": u"DDL",
            "OTHER": u"未识别语句"
        }
        return switcher.get(sqlTag, "nothing")

    def saveToExcel(self, rows):
        # 定义excel操作句柄
        excle_Workbook = Workbook()
        excel_sheet_name = time.strftime('%Y-%m-%d')
        excel_sheet = excle_Workbook.add_sheet(excel_sheet_name)
        index = 0
        # 标题
        for data in self.excel_headDatas:
            excel_sheet.write(0, index, data)
            index += 1

        index = 1

        try:
            # 内容
            for row in rows:
                colIndex = 0
                for item in range(self.excel_headDatas.__len__()):
                    excel_sheet.write(index, colIndex, row[item])
                    colIndex += 1
                index += 1
        except Exception as err:
            exstr = traceback.format_exc()
            print exstr
        # 保存test.xlsx到当前程序目录
        excle_Workbook.save('slowsql3.xls')


if __name__ == '__main__':
    slowSQL3 = SlowSQL3()
    rows = slowSQL3.getLatestWeekSlowLog
    slowSQL3.saveToExcel(rows)
