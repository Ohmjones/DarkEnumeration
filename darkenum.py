#!/usr/bin/python
import subprocess, multiprocessing, os, time, re, sys
from multiprocessing import Process, Queue

if len(sys.argv) != 2:
    print "Usage: ./http.py <targetip>"
    sys.exit(0)

ip_address = str(sys.argv[1])

def xProc(targetin, target, port):
	jobs = []
	proc = multiprocessing.Process(target=targetin, args=(target,port))
	jobs.append(proc)
	proc.start()
	return

def http(ip_address, port):
	print "[*] Launching HTTP scripts on " + ip_address
	httpscript = "~/Scripts/http.py %s" % (ip_address)
	os.system("gnome-terminal -e 'bash -c \"" + httpscript + "\";bash'")
	return

def https(ip_address, port):
	print "[*] Launching SSL scripts on " + ip_address
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
	print "[*] Running Intrusive NMAP scans against target."
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
	usout = open('/tmp/' + ip_address + '/unicorn','w')

	tcptest = "unicornscan -mT -r500 -p1-65535 -I %s" % ip_address
	calltcpscan = subprocess.Popen(tcptest, stdout=subprocess.PIPE, shell=True)
	calltcpscan.wait()

	udptest = "unicornscan -mU -r500 -p1-65535 -I %s" % ip_address
	calludpscan = subprocess.Popen(udptest, stdout=subprocess.PIPE, shell=True)
	calludpscan.wait()

	tcpservice = []
	tcpports = []
	for lines in calltcpscan.stdout:
		if re.search('\[([\s0-9{1,5}]+)\]',lines):
			linez = re.split('[\[\]\s]', lines)
			cleansrv = filter(None, linez)
			services = [cleansrv.strip() for cleansrv in cleansrv][2]
			cleanprt = filter(None, linez)
			ports = [cleanprt.strip() for cleanprt in cleanprt][3]
			tcpservice.append(services)
			tcpports.append(ports)

	tcpserv_dict = tcpservice
	tcpport_dict = tcpports
	usout.write(str(tcpserv_dict) + ":" + str(tcpport_dict) + '\n')

	udpservice = []
	udpports = []
	for lines in calludpscan.stdout:
		if re.search('\[([\s0-9{1,5}]+)\]',lines):
			linez = re.split('[\[\]\s]', lines)
			cleansrv = filter(None, linez)
			services = [cleansrv.strip() for cleansrv in cleansrv][2]
			cleanprt = filter(None, linez)
			ports = [cleanprt.strip() for cleanprt in cleanprt][3]
			udpservice.append(services)
			udpports.append(ports)

	udpserv_dict = udpservice
	udpport_dict = udpports
	usout.write(str(udpserv_dict) + ":" + str(udpport_dict) + '\n')
	usout.close()
	intrusive(ip_address)

	for service, port in zip(tcpserv_dict,tcpport_dict): 
		if ((service == "http") and (port == "80")) or ((service == "https") and (port == "443")):
			print "[!] Detected HTTP/SSL on " + ip_address + " taking the slow route to executing both http/ssl scripts..."
			if ((service == "http") and (port == "80")) or ((service == "https") and (port == "443")):
				xProc(http, ip_address, None)
				time.sleep(900) # give http 15 minutes to complete
				xProc(https, ip_address, None)
			elif (service == "http") and (port == "80"):				
				print "[!] Detected HTTP on " + ip_address + ":" + port + " (TCP)"
				xProc(http, ip_address, None)
			elif (service == "https") and (port == "443"):
				print "[!] Detected SSL on " + ip_address + ":" + port + " (TCP)"
				xProc(https, ip_address, None)
			else:
				pass
		elif (service == "ssh") and (port == "22"):
			print "[!] Detected SSH on " + ip_address + ":" + port + " (TCP)"
			xProc(ssh, ip_address, None)
		elif (service == "smtp") and (port == "25"):
			print "[!] Detected SMTP on " + ip_address + ":" + port + " (TCP)"
			xProc(smtp, ip_address, None)
		elif (service == "microsoft-ds") and (port == "445") and (port == "139"):
			print "[!] Detected Samba on " + ip_address + ":" + port + " (TCP)"
			xProc(samba, ip_address, None)
		elif (service == "ms-sql") and (port == "1433"):
			print "[!] Detected MS-SQL on " + ip_address + ":" + port + " (TCP)"
			xProc(mssql, ip_address, None)
		elif (service == "mysql") and (port == "3306"):
			print "[!] Detected MYSQL on " + ip_address + ":" + port + " (TCP)"
			xProc(mysql, ip_address, None)
	for service, port in zip(udpserv_dict,udpport_dict):
		if (service == "snmp") and (port == "161"):
			print "[!] Detected snmp on " + ip_address + ":" + port + " (UDP)"
			xProc(snmp, ip_address, None)

print "##############################################################"
print "####		       Dark Enumeration  		  ####"
print "####   HTTP, SSL, SSH, SMTP, SAMBA, MS-SQL, MYSQL, SNMP   ####"
print "####			  by: Ohm			  ####"
print "##############################################################"
 
if __name__=='__main__':
	path = os.path.join("/tmp", ip_address.strip())
	try:
		os.mkdir(path)
	except:
		pass
	unicorn(ip_address)
