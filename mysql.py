#!/usr/bin/python

import sys, os, subprocess, re, time

if len(sys.argv) != 2:
    print "Usage: mysql.py <target>"
    sys.exit(0)

ip_address = str(sys.argv[1])
NSEscripts = ["mysql-dump-hashes.nse", "mysql-empty-password.nse", "mysql-enum.nse", "mysql-vuln-cve2012-2122.nse"]

def nmap(ip_address):
	print "[*] Running non-default NSE MYSQL scripts against " + ip_address	
	for script in NSEscripts:
		if ("mysql-dump-hashes" in script):
			sqlnse = "nmap -sS -p3306 --script mysql-dump-hashes.nse --script-args='username=root,password=secret' %s -oA /tmp/%s/mysql-dump-hashes" % (ip_address, ip_address)
			subprocess.call(sqlnse, shell=True)
		elif ("mysql-empty-password" in script):
			sqlnse = "nmap -sS -p3306 --script mysql-empty-password.nse %s -oA /tmp/%s/mysql-empty-password" % (ip_address, ip_address)
			subprocess.call(sqlnse, shell=True)
		elif ("mysql-enum" in script):
			sqlnse = "nmap -sS -p3306 --script mysql-enum.nse %s -oA /tmp/%s/mysql-enum" % (ip_address, ip_address)
			subprocess.call(sqlnse, shell=True)
		elif ("mysql-vuln-cve2012-2122" in script):
			sqlnse = "nmap -sS -p3306 --script mysql-vuln-cve2012-2122.nse %s -oA /tmp/%s/mysql-vuln-cve2012-2122" % (ip_address, ip_address)
			subprocess.call(sqlnse, shell=True)

def main():
	nmap(ip_address)

if __name__=='__main__':
	main()
