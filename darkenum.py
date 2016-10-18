#!/usr/bin/python
# Script to enumerate a given list of livehosts

# Module Importations
import subprocess, multiprocessing, os, time, re
from multiprocessing import Process, Queue

# Kick off multiprocessing
def xProc(targetin, target, port):
	jobs = []
	proc = multiprocessing.Process(target=targetin, args=(target,port))
	jobs.append(proc)
	proc.start()
	return

# Kick off further enumeration.
def http(ip_address, port):
	print "[*] Launching HTTP scripts on " + ip_address
	httpscript = "~/Scripts/http.py %s" % (ip_address)
	os.system("gnome-terminal -e 'bash -c \"" + httpscript + "\";bash'")
	return

def https(ip_address, port):
	print "[*] Launching HTTPS scripts on " + ip_address
	httpsscript = "~/Scripts/https.py %s" % (ip_address)
	os.system("gnome-terminal -e 'bash -c \"" + httpsscript + "\";bash'")	
     	return

def mssql(ip_address, port):
	print "[*] Launching MSSQL scripts on " + ip_address
	mssqlscript = "~/Scripts/mssql.py %s" % (ip_address)
	os.system("gnome-terminal -e 'bash -c \"" + mssqlscript + "\"'")
     	return

def mysql(ip_address, port):
	print "[*] Launching MYSQL scripts on " + ip_address
	mysqlscript = "~/Scripts/mysql.py %s" % (ip_address)
	os.system("gnome-terminal -e 'bash -c \"" + mysqlscript + "\"'")
     	return    

def ssh(ip_address, port):
	print "[*] Launching SSH scripts on " + ip_address
	sshscript = "~/Scripts/ssh.py %s" % (ip_address)
	os.system("gnome-terminal -e 'bash -c \"" + sshscript + "\";bash'")
	return

def snmp(ip_address, port):
	print "[*] Launching SNMP scripts on " + ip_address   
	snmpscript = "~/Scripts/snmp.py %s" % (ip_address)
	os.system("gnome-terminal -e 'bash -c \"" + snmpscript + "\"'") 
	return

def smtp(ip_address, port):
	print "[*] Launching SMTP scripts on " + ip_address 
	smtpscript = "~/Scripts/smtp.py %s" % (ip_address)
	os.system("gnome-terminal -e 'bash -c \"" + smtpscript + "\";bash'")
	return

def samba(ip_address, port):
	print "[*] Launching SAMBA scripts on " + ip_address
	sambascript = "~/Scripts/samba.py %s" % (ip_address)
	os.system("gnome-terminal -e 'bash -c \"" + sambascript + "\"'")
	return

def intrusive(ip_address):
	print "[*] Unicornscan on " + ip_address + " completed. Running Intrusive NMAP scans against target."
	cmd = "nmap -Pn -sTU -pT:" + ','.join(tcpport_dict) + ",U:" + ','.join(udpport_dict) + " --open -sC -sV -O %s -oA /tmp/%s/intrusivescan" % (ip_address, ip_address)
	os.system("gnome-terminal -e 'bash -c \"" + cmd + "\"'")	

def unicorn(ip_address):
	ip_address = ip_address.strip()
	print "[*] Running initial TCP/UDP fingerprinting on " + ip_address + " [*]"
	global tcpport_dict
	global tcpserv_dict
	global udpport_dict
	global udpserv_dict
	tcpport_dict = {}
	tcpserv_dict = {}
	udpport_dict = {}
	udpserv_dict = {}
	
	#tcp scan
	tcptest = "unicornscan -mT -p1-65535 -r500 -I %s" % ip_address
	calltcpscan = subprocess.Popen(tcptest, stdout=subprocess.PIPE, shell=True)
	calltcpscan.wait()
	#udp scan 
	udptest = "unicornscan -mU -p1-65535 -r500 -I %s" % ip_address
	calludpscan = subprocess.Popen(udptest, stdout=subprocess.PIPE, shell=True)
	calludpscan.wait()

# populate tcp service names & ports
	tcpports = []
	tcpservice = []
	for lines in calltcpscan.stdout:
		if re.search('\[([\s0-9{1,5}]+)\]',lines):
			linez = re.split('\W+', lines)
			services = [x for x in linez if x][2]
			ports = [x for x in linez if x][3]
			if service not in tcpservice:
				tcpservice.append(service)
			if port not in tcpports:
				tcpports.append(port)
	tcpport_dict = tcpports
	tcpserv_dict = tcpservice

# populate udp service names & ports
	udpports = []
	udpservice = []
	for lines in calludpscan.stdout:
		if re.search('\[([\s0-9{1,5}]+)\]',lines):
			linez = re.split('\W+', lines)
			services = [x for x in linez if x][2]
			ports = [x for x in linez if x][3]
			if service not in udpservice:
				udpservice.append(service)
			if port not in udpports:
				udpports.append(port)
	
	udpport_dict = udpports
	udpserv_dict = udpservice
	
# print out unicornscan findings to a document
	usout = open('/tmp/' + ip_address + '/unicorn','w')
	try:
		usout.write(ip_address + " " + tcpserv_dict + ":" + tcpport_dict + '\n')
		usout.write(ip_address + " " + udpserv_dict + ":" + udpport_dict + '\n')
		usout.write("plug n' play manual edition:\n")
		usout.write(ip_address + "=:" + tcpport_dict + ",U:" + udpport_dict + '\n\n')
	except:
		break

# Kick off intrusive Nmap scanning
	jobs = []
	mp = multiprocessing.Process(target=intrusive, args=(ip_address,))
	jobs.append(mp)
	mp.start()

# Kick off standalone python scripts to further enumerate each service
	for service, port in zip(tcpserv_dict,tcpport_dict): 
		if (service == "http") and (port == "80"):
			print "[!] Detected HTTP on " + ip_address + ":" + port + " (TCP)"
			time.sleep(60)
			xProc(http, ip_address, None)
	
		elif (service == "https") and (port == "443"):
			print "[!] Detected SSL on " + ip_address + ":" + port + " (TCP)"
			time.sleep(240)
			xProc(https, ip_address, None)

		elif (service == "ssh") and (port == "22"):
			print "[!] Detected SSH on " + ip_address + ":" + port + " (TCP)"
			time.sleep(60)
			xProc(ssh, ip_address, None)

		elif (service == "smtp") and (port == "25"):
			print "[!] Detected SMTP on " + ip_address + ":" + port + " (TCP)"
			time.sleep(60)
			xProc(smtp, ip_address, None)

		elif (service == "microsoft-ds") and (port == "445") and (port == "139"):
			print "[!] Detected Samba on " + ip_address + ":" + port + " (TCP)"
			time.sleep(60)
			xProc(samba, ip_address, None)

		elif (service == "ms-sql") and (port == "1433"):
			print "[!] Detected MS-SQL on " + ip_address + ":" + port + " (TCP)"
			time.sleep(60)
			xProc(mssql, ip_address, None)
	
		elif (service == "mysql") and (port == "3306"):
			print "[!] Detected MYSQL on " + ip_address + ":" + port + " (TCP)"
			time.sleep(60)
			xProc(mysql, ip_address, None)			

		for service, port in zip(udpserv_dict,udpport_dict):
			if (service == "snmp") and (port == "161"):
				print "[!] Detected snmp on " + ip_address + ":" + port + " (UDP)"
				time.sleep(180)
				xProc(snmp, ip_address, None)
			elif (service == "netbios") and (port == "137") or (port == "138"):
				print "[!] Netbios detected on UDP. If nmap states the tcp port is vulnerable, run '-pT:445,U:137' to eliminate false positive"
			else:
				print "[*] Nmap intrusive scan output should be thoroughly reviewed at /tmp/" + ip_address

print "############################################################"
print "####                                                    ####"
print "####                 Dark Enumeration                   ####"
print "####                      by: Ohm                       ####"
print "############################################################"
 
if __name__=='__main__':
	targetfile = open('/tmp/livehosts', 'r')		
	for target in targetfile:
		path = os.path.join("/tmp", target.strip())
		try:		
			os.mkdir(path)
		except:
			pass
		unicorn(target)	
	targetfile.close()
