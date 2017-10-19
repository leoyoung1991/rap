# -*- coding: utf-8 -*-

import urllib
import urllib2
import re
import time


# obtain some ip and port for spider from a site,xicidaili.com.
class IPProxyPool:
    def __init__(self, region='国内普通'):

        self.region = {'国内普通': 'nt/', '国内高匿': 'nn/', '国外普通': 'wt/', '国外高匿': 'wn/', 'SOCKS': 'qq/'}

        self.url = 'http://www.xicidaili.com/' + self.region[region]
        self.header = {}
        self.header[
            'User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36'

    def get_prpxy(self):

        req = urllib2.Request(self.url, headers=self.header)
        resp = urllib2.urlopen(req)
        content = resp.read()

        self.get_ip = re.findall(r'(\d+\.\d+\.\d+\.\d+)</td>\s*<td>(\d+)</td>', content)

        self.pro_list = []
        for each in self.get_ip:
            a_info = each[0] + ':' + each[1]
            self.pro_list.append(a_info)

        return self.pro_list

    def save_pro_info(self):
        with open('proxy', 'w') as f:
            for each in self.get_ip:
                a_info = each[0] + ':' + each[1] + '\n'
                f.writelines(a_info)


if __name__ == '__main__':
    proxy = ObtainProxy()
    proxy.get_prpxy()
    proxy.save_pro_info()