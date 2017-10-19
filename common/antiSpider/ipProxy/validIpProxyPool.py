#encoding=utf8
import urllib
import socket


socket.setdefaulttimeout(3)
f = open("proxy")
lines = f.readlines()
proxys = []
for i in range(0,len(lines)):
    ip = lines[i].strip("\n").split(":")
    proxy_host = "http://"+ip[0]+":"+ip[1]
    proxy_temp = {"http":proxy_host}
    proxys.append(proxy_temp)
# url = "http://ip.chinaz.com/getip.aspx"
url = "http://music.163.com/playlist?id=878347174"

f = open("valid_proxy", "w")

for i in range(0,len(lines)):
    ip = lines[i].strip("\n").split(":")
    proxy_host = "http://"+ip[0]+":"+ip[1]
    proxy_temp = {"http":proxy_host}
    try:
        res = urllib.urlopen(url,proxies=proxy_temp).read()
        # 能正常获得response， 进入valid list

        f.writelines(ip[0]+":"+ip[1]+'\n')

        print res
        print proxy_temp
    except Exception,e:
        # [Errno socket error] timed out 等都会走异常
        print proxy_temp
        print e
        continue