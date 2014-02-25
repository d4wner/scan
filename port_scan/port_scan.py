#! /usr/bin/env python
#coding = utf-8
import socket
import sys
import threading
import time

NORMAL = 0
ERROR = 1
TIMEOUT =5
ip_dic = open("ip.txt","r")
rlog = open("result.log","w")
if len(sys.argv)<4:
    print 'Usage ==>[python port_scan.py urlbegin portbegin portend timeout]'
    sys.exit()
def ping(ip,port,timeout=TIMEOUT):
	try:
		# import pdb;pdb.set_trace()
		cs=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		cs.settimeout(float(timeout))
		address=(str(ip),int(port))
		#print address
		# status=cs.connect_ex((address))
		status=cs.connect(address)
	except Exception,e:
		#print ERROR
		print "[!]Failed at %d"%port 
		print "error:%s"%e
		return ERROR
	else:
		print "[+]%d is NORMAL"%port
		rlog.writelines('[+]'+ip+':'+str(port)+' open\n')
	finally:
		cs.close()

class Scan(threading.Thread):
	def __init__(self,ip,timeout):
		threading.Thread.__init__(self)
		self.ip=ip
		self.timeout=timeout

	def run(self):
		global p_begin,p_end,mutex
		threadname=threading.currentThread().getName()
		while 1:
			#print 'start'
			mutex.acquire()
			if p_begin>p_end:
				mutex.release()
				break
			ping(self.ip,p_begin,self.timeout)
			p_begin+=1
			mutex.release()

if __name__=='__main__':
    while ip_dic.readline():
		#urlbegin = str(sys.argv[1])
        ip = ip_dic.readline()
        print '[+]'+ip
        urlbegin = ip.strip('\n')	
        portbegin = int(sys.argv[1])
        portend = int(sys.argv[2])
        timeout = float(sys.argv[3])
		
        global p_begin,p_end,mutex
        threads = []
        num = 1
        p_begin = portbegin
        p_end = portend

        mutex = threading.Lock()
        for x in xrange(0,num):
            #print x
            t_scan = Scan(urlbegin,timeout)
		    #t_scan.setDaemon(True)
            threads.append(t_scan)
        for t in threads:
            t.start()
        for t in threads:
            t.join()
		






