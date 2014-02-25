#!/usr/bin/env python
#coding=utf-8
import os
import re
import time
import sys
from threading import Thread

ip_dic = open('ip.txt','w')
if len(sys.argv) < 2:
    print 'Usage ===> [python simple_scan.py 192.168.227.]\n'
    sys.exit()
ip_pre = sys.argv[1]
class testit(Thread):
    def __init__ (self,ip):
        Thread.__init__(self)
        self.ip = ip
        self.status = -1
    def run(self):
        pingaling = os.popen("ping -q -c2 "+self.ip,"r")
        while 1:
          line = pingaling.readline()
          if not line: break
          igot = re.findall(testit.lifeline,line)
          if igot:
             self.status = int(igot[0])
  
testit.lifeline = re.compile(r"(\d) received")
  
print time.ctime()
  
pinglist = []
  
for host in range(0,255):
    ip = ip_pre+str(host)
    current = testit(ip)
    pinglist.append(current)
    current.start()
  
for pingle in pinglist:
    pingle.join()
    if pingle.status != 0:
		print "[!] ",pingle.ip," exsit."
		ip_dic.writelines(pingle.ip+'\n')
    else:
        continue
  
if __name__ == '__main__':
    print time.ctime()

