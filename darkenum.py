#!/usr/bin/python
import subprocess, multiprocessing, os, time, re, sys, collections
from multiprocessing import Process, Queue
from intro import intro

if len(sys.argv) != 2:
    print "Usage: ./darkenum.py <targetip>"
    sys.exit(0)

ip_address = str(sys.argv[1])

def intrusive(ip_address):
	print "[*] Running Intrusive NMAP scans against target."
	cmd = "nmap -Pn -sTU -pT:" + ",".join(map(str, tports)) + ",U:" + ",".join(map(str, uports)) + " --open -sC -sV -O %s -oA /tmp/%s/intrusivescan" % (ip_address, ip_address)
	print "Running Intrusive Nmap script:"
	print cmd
	os.system("gnome-terminal -e 'bash -c \"" + cmd + "\"'")	

def unicorn(ip_address):
	ip_address = ip_address.strip()
	print "[*] Running initial TCP/UDP fingerprinting on " + ip_address + " [*]"

	'''
	Collections of data values
	'''

	global tcp_dict
	global udp_dict
	global tports
	global uports
	tports = []
	uports = []
	tcp_dict = collections.defaultdict(list)
	udp_dict = collections.defaultdict(list)

	'''
	TCP full port scan
	'''

	tcptest = "unicornscan -mT -r500 -p1-65535 -I %s" % ip_address
	calltcpscan = subprocess.Popen(tcptest, stdout=subprocess.PIPE, shell=True)
	calltcpscan.wait()

	'''
	UDP full port scan
	'''

	udptest = "unicornscan -mU -r500 -p1-65535 -I %s" % ip_address
	calludpscan = subprocess.Popen(udptest, stdout=subprocess.PIPE, shell=True)
	calludpscan.wait()

	'''
	TCP service:port clean-up and append data to tports & tcp_dict
	'''

	for lines in calltcpscan.stdout:
		if re.search('\[([\s0-9{1,5}]+)\]',lines):
			linez = re.split('[\[\]\s]', lines)
			cleansrv = filter(None, linez)
			services = [cleansrv.strip() for cleansrv in cleansrv][2]
			cleanprt = filter(None, linez)
			ports = [cleanprt.strip() for cleanprt in cleanprt][3]
			tcp_dict[services].append(ports)

	if tcp_dict:
		for key, val in tcp_dict.iteritems():
			vals = ','.join(val[0:])
			tports.append(vals)
	else:
		print "there were no open tcp ports..." + "\n"

	'''
	UDP service:port clean-up and append data to uports & udp_dict
	'''

	for lines in calludpscan.stdout:
		if re.search('\[([\s0-9{1,5}]+)\]',lines):
			linez = re.split('[\[\]\s]', lines)
			cleansrv = filter(None, linez)
			services = [cleansrv.strip() for cleansrv in cleansrv][2]
			cleanprt = filter(None, linez)
			ports = [cleanprt.strip() for cleanprt in cleanprt][3]
			udp_dict[services].append(ports)

	if udp_dict:
		for key, val in udp_dict.iteritems():
			vals = ','.join(val[0:])
			uports.append(vals)
	else:
		print "there were no open udp ports..." + "\n"

	intrusive(ip_address)

 
if __name__=='__main__':
	path = os.path.join("/tmp", ip_address.strip())
	intro()
	try:
		print "Attempting to create directory: '" + path + "/' ..."
		os.mkdir(path)
	except:
		print "Directory '" + path + "/' already exists, skipping step..."
		pass

	unicorn(ip_address)
