#!/usr/bin/python
import datetime, subprocess, multiprocessing, os, time, re, sys, collections
from multiprocessing import Process, Queue
from intro import intro
from datetime import date

if len(sys.argv) != 2:
    print "Usage: ./darkenum.py <targetip>"
    sys.exit(0)

ip_address = str(sys.argv[1])

def intrusive(ip_address):
	print "\t[!] Running Service Version, Default Scripts, Operating System Detection and Traceroute NMAP scans against target."
	params = ' --open -A %s -oA /tmp/%s/intrusivescan' % (ip_address, ip_address)

	if tcp_dict and udp_dict:
		cmd = "nmap -Pn -sS -pT:" + ",".join(map(str, tports)) + ",U:" + ",".join(map(str, uports)) + params + "\n"
		print "Running Nmap syntax: " + cmd

	elif tcp_dict and not udp_dict:
		cmd = "nmap -Pn -sS -pT:" + ",".join(map(str, tports)) + params + "\n"
		print "Running Nmap syntax: " + cmd

	elif udp_dict and not tcp_dict:
		cmd = "nmap -Pn -sU -pU:" + ",".join(map(str, uports)) + params + "\n"
		print "Running Nmap syntax: " + cmd

        os.system("gnome-terminal -e 'bash -c \"" + cmd + "\"'")	

def uscan(ip_address):
	ip_address = ip_address.strip()
	print "\n[!] Running initial Unicornscan TCP/UDP fingerprinting on " + ip_address + " [*]"
	print "\t[!] Starting scans on " + str(datetime.datetime.fromtimestamp(time.time()).strftime("%A %B %d, %Y at %H:%M:%S"))

	'''
	Creation of Variables
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

	tcptest = "unicornscan -mT -r700 -p1-65535 -I %s" % ip_address
	calltcpscan = subprocess.Popen(tcptest, stdout=subprocess.PIPE, shell=True)
	calltcpscan.wait()
	print "\t[!] Unicornscan finished for all 65,535 TCP ports, timestamped: " + str(datetime.datetime.fromtimestamp(time.time()).strftime("%H:%M:%S"))

	'''
	UDP full port scan
	'''

	udptest = "unicornscan -mU -r700 -p1-65535 -I %s" % ip_address
	calludpscan = subprocess.Popen(udptest, stdout=subprocess.PIPE, shell=True)
	calludpscan.wait()
        print "\t[!] Unicornscan finished for all 65,535 UDP ports, timestamped: " + str(datetime.datetime.fromtimestamp(time.time()).strftime("%H:%M:%S"))

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
			if ports in tcp_dict.iteritems():
				pass
			elif ports not in tcp_dict:
				tcp_dict[services].append(ports)
			else:
				pass

	if tcp_dict:
		for key, val in tcp_dict.iteritems():
			if val not in tports:
				vals = ','.join(val[0:])
				tports.append(vals)
	else:
		print "\t[!] There were no open TCP ports..." + "\n"

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
			if ports in udp_dict.iteritems():
				pass
			elif ports not in udp_dict:
				udp_dict[services].append(ports)
			else:
				pass

	if udp_dict:
		for key, val in udp_dict.iteritems():
			if val not in uports:
				vals = ','.join(val[0:])
				uports.append(vals)
	else:
		print "\t[!] There were no open UDP ports..." + "\n"

	'''
	Print unicorn scan results to a document, namely for record keeping.
	'''
	pathfp = path + "/unicorn_results.txt"
	ffile = open(pathfp, "w")
	ffile.write(str(tcp_dict))
	ffile.write("\n")
	ffile.write(str(udp_dict))
	ffile.close()

	intrusive(ip_address)

if __name__=='__main__':
	path = os.path.join("/tmp", ip_address.strip())
	intro()
	try:
		print "[!] Attempting to create directory: '" + path + "/'"
		os.mkdir(path)
		print "\t[!] Directory " + path + "/ created successfully!"
	except:
		print "\t[!] Directory '" + path + "/' already exists, skipping step..."
		pass

	uscan(ip_address)
